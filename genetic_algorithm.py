import random
import math

def generate_population(ukuran, ukuran_variabel):
    populasi = []
    for i in range(ukuran):
        individu = {
            "x": [int(random.choice([1, 0])) for j in range(ukuran_variabel)],
            "y": [int(random.choice([1, 0])) for j in range(ukuran_variabel)]
        }
        populasi.append(individu)

    return populasi


def decode_kromosom(individu):
    x = individu['x']
    y = individu['y']

    def rumus_part(var):
        part1, part2 = (0, 0)
        for i in range(len(var)):
            part1 += 2**-(i+1)
            part2 += var[i]*(2**-(i+1))

        return part1, part2

    def rumus(part1, part2, batas):
        batas_bawah, batas_atas = batas
        return batas_bawah+((batas_atas-batas_bawah)/part1)*part2

    part1, part2 = rumus_part(x)
    nilai_x = rumus(part1, part2, BATAS_X)
    part1, part2 = rumus_part(y)
    nilai_y = rumus(part1, part2, BATAS_Y)
    return nilai_x, nilai_y


def hitung_fitness(individu):
    x, y = decode_kromosom(individu)
    return (math.cos(x**2) * math.sin(y**2)) + (x + y)


def sorting_populasi_by_fitness(populasi):
    return sorted(populasi, key=hitung_fitness, reverse=True)


def tournament_selection(populasi):
    parent = random.choices(populasi, k=5)
    parent = sorting_populasi_by_fitness(parent)
    return parent[0]

def crossover(p1, p2, pc):
    if random.random() < pc:
        kromosom_p1 = p1['x'] + p1['y']
        kromosom_p2 = p2['x'] + p2['y']
        titik = random.choice(range(0, len(kromosom_p1)))
        anak1 = kromosom_p1[0:titik] + kromosom_p2[titik:]
        anak2 = kromosom_p2[0:titik] + kromosom_p1[titik:]
        p1 = {'x': anak1[:(len(kromosom_p1) // 2)], 'y': anak1[(len(kromosom_p1) // 2):]}
        p2 = {'x': anak2[:(len(kromosom_p1) // 2)], 'y': anak1[(len(kromosom_p1) // 2):]}
    return p1, p2

def mutasi(offspring, pm):
    kromosom = offspring['x'] + offspring['y']
    for i in range(len(kromosom)):
        if random.random() <= pm:
            kromosom[i] = 0 if kromosom[i] == 1 else 1
    hasil_mutasi = {'x': kromosom[:(len(kromosom)//2)], 'y': kromosom[(len(kromosom)//2):]}
    return hasil_mutasi

def elitism(populasi, jumlah):
    populasi_terurut = sorting_populasi_by_fitness(populasi)
    kaum_elit = [populasi_terurut[i] for i in range(jumlah)]
    return kaum_elit

def pergantian_generasi(populasi_sebelumnya):
    populasi_baru = elitism(populasi_sebelumnya, JUMLAH_INDIVIDU_ELIT)
    while len(populasi_baru) < UKURAN_POPULASI:
        parent1 = tournament_selection(populasi)
        parent2 = tournament_selection(populasi)
        offspring1, offspring2 = crossover(parent1, parent2, PROBABILITAS_CROSSOVER)
        offspring1 = mutasi(offspring1, PROBABILITAS_MUTASI)
        offspring2 = mutasi(offspring2, PROBABILITAS_MUTASI)
        populasi_baru.extend([offspring1, offspring2])
    return populasi_baru


if __name__ == '__main__':

    BATAS_X = (-1, 2)
    BATAS_Y = (-1, 1)
    UKURAN_VARIABEL_KROMOSOM = 10
    UKURAN_POPULASI = 20
    JUMLAH_GENERASI = 30
    PROBABILITAS_CROSSOVER = 0.9
    PROBABILITAS_MUTASI = 0.1
    JUMLAH_INDIVIDU_ELIT = 2

    populasi = generate_population(UKURAN_POPULASI, UKURAN_VARIABEL_KROMOSOM)

    for generasi in range(JUMLAH_GENERASI):
        print(f'🧬 GENERASI KE-{generasi+1}')
        for individu in populasi:
            print(f'{individu} | -> {hitung_fitness(individu)}')

        populasi = pergantian_generasi(populasi)

    individu_terbaik = sorting_populasi_by_fitness(populasi)[0]
    nilai_x, nilai_y = decode_kromosom(individu_terbaik)
    nilai_fitness = hitung_fitness(individu_terbaik)
    print("==============================================")
    print('\nDidapatkan hasil akhir yang terbaik:')
    print(f'Kromosom: {individu_terbaik}')
    print(f'Dengan x = {nilai_x} dan y = {nilai_y} di dapatkan nilai fitness = {nilai_fitness}')








