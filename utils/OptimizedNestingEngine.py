import matplotlib.pyplot as plt
import matplotlib.patches as patches

class OptimizedNestingEngine:
    def __init__(self, fabric_width, margin):
        self.fabric_width = fabric_width
        self.margin = margin
        self.placed_pieces = []
        self.shelves = [] # Liste de dictionnaires {'y_start': , 'height': , 'x_used': }

    def pack(self, raw_pieces):
        # 1. Préparation et calcul de l'encombrement total (avec marge)
        pieces = []
        for p in raw_pieces:
            w_total = p['w'] + 2 * self.margin
            h_total = p['h'] + 2 * self.margin
            # Rotation automatique : on s'assure que la pièce est "couchée" 
            # si cela aide à la faire rentrer dans la laize
            if w_total > self.fabric_width and h_total <= self.fabric_width:
                w_total, h_total = h_total, w_total
            
            pieces.append({
                'name': p['name'],
                'w': w_total,
                'h': h_total,
                'pure_w': p['w'],
                'pure_h': p['h']
            })

        # 2. Tri par hauteur décroissante (fondamental pour les étagères)
        pieces.sort(key=lambda x: x['h'], reverse=True)

        for p in pieces:
            placed = False
            # Tenter de placer dans une étagère existante
            for shelf in self.shelves:
                if shelf['x_used'] + p['w'] <= self.fabric_width and p['h'] <= shelf['height']:
                    self._add_to_shelf(shelf, p)
                    placed = True
                    break
            
            # Sinon, créer une nouvelle étagère
            if not placed:
                new_y = sum(s['height'] for s in self.shelves)
                new_shelf = {'y_start': new_y, 'height': p['h'], 'x_used': 0}
                self.shelves.append(new_shelf)
                self._add_to_shelf(new_shelf, p)

    def _add_to_shelf(self, shelf, piece):
        self.placed_pieces.append({
            'name': piece['name'],
            'x': shelf['x_used'] + self.margin,
            'y': shelf['y_start'] + self.margin,
            'w': piece['pure_w'],
            'h': piece['pure_h']
        })
        shelf['x_used'] += piece['w']

    def visualize(self):
        total_height = sum(s['height'] for s in self.shelves)
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.add_patch(patches.Rectangle((0, 0), self.fabric_width, total_height, color='#f0f0f0'))
        
        for p in self.placed_pieces:
            ax.add_patch(patches.Rectangle((p['x'], p['y']), p['w'], p['h'], 
                                         edgecolor='#2c3e50', facecolor='#3498db', alpha=0.8))
            ax.text(p['x']+p['w']/2, p['y']+p['h']/2, p['name'], ha='center', va='center', fontsize=8)

        plt.xlim(0, self.fabric_width)
        plt.ylim(0, total_height)
        plt.gca().invert_yaxis()
        plt.title(f"Placement Sécurisé - Tissu utilisé : {total_height}mm")
        plt.show()

# Utilise cette classe dans ton main() à la place de la précédente