from utils.OptimizedNestingEngine import OptimizedNestingEngine
from utils.SmartRotationEngine import SmartRotationEngine
from utils.BalancedRotationEngine import BalancedRotationEngine

def main():
    # Ton entrée texte
    input_text = "Dos: 50x80, Devant: 50x80, MancheL: 30x50, MancheR: 30x50, Col: 20x10, Poche1: 15x15, Poche2: 15x15"
    marge_client = 1
    laize_tissu = 140 

    # Parsing
    raw_pieces = []
    for item in input_text.split(','):
        name, dims = item.split(':')
        w, h = map(int, dims.strip().split('x'))
        raw_pieces.append({'name': name.strip(), 'w': w, 'h': h})

    # Utilisation du nouveau moteur
    engine = OptimizedNestingEngine(laize_tissu, marge_client)
    engine.pack(raw_pieces)
    engine.visualize()

    engine_rot = SmartRotationEngine(laize_tissu, marge_client)
    engine_rot.pack(raw_pieces)
    engine_rot.visualize()

    engine_rot_2 = BalancedRotationEngine(laize_tissu, marge_client)
    engine_rot_2.pack(raw_pieces)
    engine_rot_2.visualize()

if __name__ == "__main__":
    main()
