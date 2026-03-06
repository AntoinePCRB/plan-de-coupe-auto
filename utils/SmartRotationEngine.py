import matplotlib.pyplot as plt
import matplotlib.patches as patches

class SmartRotationEngine:
    def __init__(self, fabric_width, margin):
        self.fabric_width = fabric_width
        self.margin = margin
        self.placed_pieces = []
        self.shelves = [] # {'y_start': , 'height': , 'x_used': }

    def pack(self, raw_pieces):
        # 1. On prépare les pièces (on ne fixe pas W et H tout de suite)
        pieces_to_place = []
        for p in raw_pieces:
            pieces_to_place.append({
                'name': p['name'],
                'w': p['w'] + 2 * self.margin,
                'h': p['h'] + 2 * self.margin,
                'orig_w': p['w'],
                'orig_h': p['h']
            })

        # 2. Tri par la plus grande dimension décroissante
        # Cela permet de gérer les plus gros éléments d'abord
        pieces_to_place.sort(key=lambda x: max(x['w'], x['h']), reverse=True)

        for p in pieces_to_place:
            placed = False
            
            # --- STRATÉGIE DE ROTATION ---
            # On définit les deux options possibles pour cette pièce
            opt1 = {'w': p['w'], 'h': p['h']}
            opt2 = {'w': p['h'], 'h': p['w']} # Rotation 90°
            
            # Liste des options valides (qui ne dépassent pas la laize)
            options = []
            if opt1['w'] <= self.fabric_width: options.append(opt1)
            if opt2['w'] <= self.fabric_width: options.append(opt2)

            # On essaie de placer dans les étagères existantes d'abord
            # On privilégie l'option qui rentre dans une étagère sans en créer une
            for shelf in self.shelves:
                for opt in options:
                    if shelf['x_used'] + opt['w'] <= self.fabric_width and opt['h'] <= shelf['height']:
                        self._add_to_shelf(shelf, opt, p['name'])
                        placed = True
                        break
                if placed: break

            # Si aucune étagère existante ne convient, on en crée une nouvelle
            # On choisit l'option qui crée l'étagère la moins haute pour économiser du tissu
            if not placed and options:
                best_opt = min(options, key=lambda x: x['h'])
                new_y = sum(s['height'] for s in self.shelves)
                new_shelf = {'y_start': new_y, 'height': best_opt['h'], 'x_used': 0}
                self.shelves.append(new_shelf)
                self._add_to_shelf(new_shelf, best_opt, p['name'])

    def _add_to_shelf(self, shelf, opt, name):
        # On enregistre la pièce en soustrayant la marge pour l'affichage
        self.placed_pieces.append({
            'name': name,
            'x': shelf['x_used'] + self.margin,
            'y': shelf['y_start'] + self.margin,
            'w': opt['w'] - 2 * self.margin,
            'h': opt['h'] - 2 * self.margin
        })
        shelf['x_used'] += opt['w']

    def visualize(self):
        total_height = sum(s['height'] for s in self.shelves)
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.add_patch(patches.Rectangle((0, 0), self.fabric_width, total_height, color='#f1f2f6'))
        
        for p in self.placed_pieces:
            ax.add_patch(patches.Rectangle((p['x'], p['y']), p['w'], p['h'], 
                                         edgecolor='#2c3e50', facecolor='#3498db', alpha=0.8, lw=1.5))
            ax.text(p['x']+p['w']/2, p['y']+p['h']/2, f"{p['name']}\n{int(p['w'])}x{int(p['h'])}", 
                    ha='center', va='center', fontsize=8, color='white', fontweight='bold')

        plt.xlim(0, self.fabric_width)
        plt.ylim(0, max(100, total_height))
        plt.gca().invert_yaxis()
        plt.title(f"Optimisation avec Rotations - Tissu utilisé : {total_height}mm")
        plt.show()
