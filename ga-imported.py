import ga

num_generations = 5

num_parents_meeting = 4
for generation in range(num_generations):
    fitness = ga.cal_pop_fitness(equation_inputs, new_population)
    parents = ga.select_mating_pool(
        new_population, fitness, num_parents_meeting)
    offspring_crossover = ga.crossover(parents, offspring_size=(
        pop_size[0]-parents.shape[0], num_weights))
    offspring_mutation = ga.mutation(offspring_crossover)
    new_population[0:parents.shape[0], :] = parents
    new_population[parents.shape[0]:, :] = offspring_mutation
