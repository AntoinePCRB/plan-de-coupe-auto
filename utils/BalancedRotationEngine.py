import matplotlib.pyplot as plt
import matplotlib.patches as patches

class BalancedRotationEngine:
    def __init__(self, fabric_width, margin):
        self.fabric_width = fabric_width
        self.margin = margin
        self.placed_pieces = []
        self.shelves = [] # {'y_start': , 'height': , 'x_used': }

    def pack(self, raw_pieces):
        pieces_to_place = []
        for p in raw_pieces:
            pieces_to_place.append({
                'name': p['name'],
                'w': p['w'] + 2 * self.margin,
                'h': p['h'] + 2 * self.margin,
                'pure_w': p['w'],
                'pure_h': p['h']
            })

        # Tri par hauteur originale décroissante
        pieces_to_place.sort(key=lambda x: x['h'], reverse=True)

        for p in pieces_to_place:
            placed = False
            
            # 1. TENTATIVE SANS ROTATION (Priorité 1)
            # On cherche une étagère où elle rentre dans son sens original
            for shelf in self.shelves:
                if shelf['x_used'] + p['w'] <= self.fabric_width and p['h'] <= shelf['height']:
                    self._add_to_shelf(shelf, p['w'], p['h'], p['name'])
                    placed = True
                    break
            
            if placed: continue

            # 2. TENTATIVE AVEC ROTATION (Priorité 2 - Sauvetage)
            # On ne tourne que si ça permet de boucher un trou existant
            p_rot_w, p_rot_h = p['h'], p['w'] # On inverse
            if p_rot_w <= self.fabric_width:
                for shelf in self.shelves:
                    if shelf['x_used'] + p_rot_w <= self.fabric_width and p_rot_h <= shelf['height']:
                        self._add_to_shelf(shelf, p_rot_w, p_rot_h, p['name'])
                        placed = True
                        break

            if placed: continue

            # 3. CRÉATION NOUVELLE ÉTAGÈRE
            # Ici on compare : est-ce que l'orientation originale ou tournée 
            # consomme le moins de hauteur sur le rouleau ?
            opt1_h = p['h']
            opt2_h = p_rot_h if p_rot_w <= self.fabric_width else float('inf')
            
            # On choisit l'orientation la plus courte en hauteur pour économiser le tissu
            final_w, final_h = (p['w'], p['h']) if opt1_h <= opt2_h else (p_rot_w, p_rot_h)
            
            new_y = sum(s['height'] for s in self.shelves)
            new_shelf = {'y_start': new_y, 'height': final_h, 'x_used': 0}
            self.shelves.append(new_shelf)
            self._add_to_shelf(new_shelf, final_w, final_h, p['name'])

    def _add_to_shelf(self, shelf, w, h, name):
        self.placed_pieces.append({
            'name': name,
            'x': shelf['x_used'] + self.margin,
            'y': shelf['y_start'] + self.margin,
            'w': w - 2 * self.margin,
            'h': h - 2 * self.margin
        })
        shelf['x_used'] += w

    def visualize(self):
        total_height = sum(s['height'] for s in self.shelves)
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.add_patch(patches.Rectangle((0, 0), self.fabric_width, total_height, color='#f8f9fa'))
        
        for p in self.placed_pieces:
            ax.add_patch(patches.Rectangle((p['x'], p['y']), p['w'], p['h'], 
                                         edgecolor='#2c3e50', facecolor='#3498db', alpha=0.8))
            ax.text(p['x']+p['w']/2, p['y']+p['h']/2, f"{p['name']}", 
                    ha='center', va='center', fontsize=8, color='white')

        plt.xlim(0, self.fabric_width)
        plt.ylim(0, max(1, total_height))
        plt.gca().invert_yaxis()
        plt.title(f"Optimisation Équilibrée - Longueur : {total_height}mm")
        plt.show()
