# Melakukan Import Library Random, Serta Math untuk operasi sin dan cos
import random
from math import sin, cos

# Membuat array untuk data limit x dan y
x_limit = [-1, 2]
y_limit = [-1, 1]

# Fungsi pembuatan populasi beserta kromosomnya
def generate_population(p, k):
    return [[random.randint(0,9) for _ in range(k)] for _ in range(p)]

# Fungsi membagi kromosom menjadi 2 bagian
def split_kromosom(kromosom):
    split = len(kromosom) // 2
    return kromosom[:split], kromosom[split:]

# Fungsi rumus yang akan dicari nilai maksimumnya
def function(x,y):
    return (cos(x**2) * sin(y**2)) + (x + y)

# Fungsi decode untuk setiap kromosom pada populasi
def decode(kromosom, limit) :
    kali, pembagi = 0, 0
    for i in range(len(kromosom)) :
        num = kromosom[i]
        kali += num * (10**-(i+1))
        pembagi += 9 * (10**-(i+1))

    return limit[0] + (((limit[1] - limit[0]) / pembagi) * kali)

# Fungsi untuk menentukan kromosom terbaik
def best_kromosom_selection(population):
    max_fitness = -999
    
    for kromosom in population:
        kromosom_a, kromosom_b = split_kromosom(kromosom)
        x1 = decode(kromosom_a, x_limit)
        x2 = decode(kromosom_b, y_limit)
        fitness = function(x1, x2)
        
        if  max_fitness < fitness:
            max_fitness = fitness
            max_kromosom = kromosom
      
    return max_kromosom, max_fitness, x1, x2

# Fungsi untuk melakukan proses seleksi orang tua
def parent_roulette_selection(population, fitness, fitness_total):
    r = random.random()
    i = 0
    while r > 0:
      r -= fitness[i]/fitness_total
      i += 1
      if  i == len(population) - 1:
          break
          
    return population[i]

# Fungsi untuk melakukan proses crossover anak
def crossover(parent_1, parent_2) :         
    child_1, child_2, childs = [], [], []
    pc = random.random()

    if pc < 0.9:
      child_1[:1], child_1[1:] = parent_1[:1], parent_2[1:]   
      child_2[:1], child_2[1:] = parent_2[:1], parent_1[1:]
      childs.append(child_1)
      childs.append(child_2)
    else:   
      childs.append(parent_1)
      childs.append(parent_2)

    return childs

# Fungsi untuk melakukan proses mutasi anak
def mutation(child_1, child_2):
    for i in range(len(child_1)):
        p = random.random()
        if p < 0.1:
           child_1[i] = random.randint(0,9)

        q = random.random()
        if q < 0.1:
           child_2[i] = random.randint(0,9)
           
    return child_1, child_2

# Fungsi elitisme untuk memasukkan kromosom terbaik pada generasi sebelumnya
def elitisme(population, best_kromosom_generation, bad_kromosom, total_fitness):
    if  best_kromosom_generation[1] > bad_kromosom[0] and (best_kromosom_generation[0] not in population):
        population[bad_kromosom[2]] = best_kromosom_generation[0]
        total_fitness = (total_fitness - bad_kromosom[0]) + best_kromosom_generation[1]
        
        print('\nProses Elitisme')
        print(f'Kromosom Ke-{bad_kromosom[2]+1}: {bad_kromosom[1]}, fitness: {bad_kromosom[0]}')
        print(f'diubah menjadi {best_kromosom_generation[0]}, fitness: {best_kromosom_generation[1]}\n')

    return population, total_fitness

# Inisialisasi Jumlah populasi, generasi serta pemanggilan fungsi untuk membuat populasi
generation = 100
population_total = 10
kromosom_total = 6

population = generate_population(population_total, kromosom_total)
print("Populasi Awal:", population)

best_kromosom_generation = []

# Perulangan untuk melakukan proses seleksi populasi
for gen in range(generation):

      # Inisialisasi variabel untuk proses perhitungan algoritma genetika
      kromosom_data, best_kromosom, bad_kromosom, fitness_data, new_population, child = [], [], [], [], [], []
      total_fitness, count_kromosom, index = 0, 999, 0
      
      print('\n================================================================')
      print('Generasi', gen+1)
      print('=================================================================')
      # Perulangan untuk mencari nilai phenotype dan nilai fungsi / fitness pada setiap kromosom 
      for i, kromosom in enumerate(population):                         
          kromosom_a, kromosom_b = split_kromosom(kromosom)
          x1 = decode(kromosom_a, x_limit)
          x2 = decode(kromosom_b, y_limit)

          fitness_value = function(x1, x2)
          fitness_data.append(fitness_value)
          total_fitness += fitness_value
          
          # Pencarian Fitness Terkecil Dalam Suatu Generasi
          if gen != 0 and fitness_value < count_kromosom:
                  count_kromosom = fitness_value
                  bad_kromosom = [fitness_value, kromosom, i]

             
      # Pemilihan Kromosom Dengan Fitness Terbaik
      best_kromosom = best_kromosom_selection(population)

      print("Kromosom Terbaik :", best_kromosom[0])
      print("Fitness Terbaik :", best_kromosom[1])

      # Proses Elitisme untuk memasukkan kromosom terbaik pada generasi sebelumnya
      if gen != 0:
         most_best = sorted(best_kromosom_generation, key=lambda x: x[1], reverse=True)[0]
         population, total_fitness = elitisme(population, most_best, bad_kromosom, total_fitness)

      best_kromosom_generation.append(best_kromosom)

      # Perulangan untuk melakukan seleksi orang tua, crossover dan mutasi anak untuk mendapatkan populasi generasi selanjutnya
      if  gen != generation-1 :
          for i in range(population_total // 2):
              parent_1 = parent_roulette_selection(population, fitness_data, total_fitness)
              parent_2 = parent_roulette_selection(population, fitness_data, total_fitness)

              childs = crossover(parent_1, parent_2)
              child_1, child_2 = mutation(childs[0], childs[1])

              new_population.append(child_1)
              new_population.append(child_2)

          population = new_population

# Memanggil fungsi untuk menentukan kromosom terbaik pada keseluruhan generasi
print('\n=====================================================')
print('Hasil Akhir Kromosom Terbaik')
print('=====================================================')
print('Kromosom Terbaik         = ', most_best[0])
print('Phenotype x              = ', most_best[2])
print('Phenotype y              = ', most_best[3])
print('Nilai Fungsi / Fitness   = ', most_best[1])
print('=====================================================')

"""
Solution Optima
Max : 2.44998, (x, y) = (2, 1)
Max : 2.48173, (x, y) = (0.87, 1)
"""