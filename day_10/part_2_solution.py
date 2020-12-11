import itertools
from progress.bar import Bar # for the fancy progress bar
import time # for calculating estimated completion time

#==============================================================================
# Generate class for the fancy completion bar

class FancyBar(Bar):
    message = 'Processing'
    fill = '#'
    suffix = '%(percent).1f%% - %(remaining_hours)dh %(remaining_minutes)dm %(remaining_seconds)ds' # %(remaining_minutes)dm
    @property
    def remaining_hours(self):
        return self.eta // 3600
    @property
    def remaining_minutes(self):
        return (self.eta % 3600) // 60
    @property
    def remaining_seconds(self):
        return ((self.eta % 3600) % 60)

#==============================
print('Performing Setup...')


puzzle_input = []

with open('puzzle_input') as infile:
    for line in infile:
        puzzle_input.append(int(line.rstrip('\n')))

def find_max_joltage(adapter_list):

    return max(adapter_list) + 3

def find_next_adapter(current_adapter, adapter_list):

    increase = 1
    match = False
    error = False

    while not match and not error:

        if current_adapter + increase in adapter_list and increase <= 3:

            match = True

        elif increase <= 3:

            increase += 1

        else:

            error = True

    if match:

        return current_adapter + increase, increase

    else:

        return False

def find_adapter_sequence(adapter_list):

    current_adapter = 0
    max_joltage = find_max_joltage(adapter_list)
    adapter_sequence = [0]
    jolt_differences = []
    error = False

    while current_adapter != max_joltage - 3 and not error:

        if bool(find_next_adapter(current_adapter, adapter_list)):

            current_adapter, jolt_difference = find_next_adapter(current_adapter, adapter_list)

            adapter_sequence.append(current_adapter)
            jolt_differences.append(jolt_difference)

        else:

            error = True

    if not error:

        # add on the final 3 to meet the max_joltage
        jolt_differences.append(3)

        # add on the joltage goal to the adapter sequence
        adapter_sequence.append(max_joltage)

        return adapter_sequence, jolt_differences

    else:

        return False

def find_vital_adapters(adapter_list):

    adapter_sequence, jolt_differences = find_adapter_sequence(adapter_list)

    vital_set = {0}

    for index, j in enumerate([i == 3 for i in jolt_differences]):
        if j:
            vital_set.add(adapter_sequence[index])
            vital_set.add(adapter_sequence[index+1])

    return vital_set

def find_nonvital_adapters(adapter_list, vital_adapters):

    return set(adapter_list).difference(vital_adapters)

def check_adapter_sequence_validity(adapter_list):

    current_adapter = 0
    max_joltage = find_max_joltage(adapter_list)
    error = False

    while current_adapter != max_joltage - 3 and not error:

        if bool(find_next_adapter(current_adapter, adapter_list)):

            current_adapter, jolt_difference = find_next_adapter(current_adapter, adapter_list)

        else:

            error = True

    if not error:

        return True

    else:

        return False

# this function (from stack overflow, https://stackoverflow.com/questions/464864/how-to-get-all-possible-combinations-of-a-list-s-elements)
    # returns all combinations of a set, including 0 elements and all elements.
    # not totally sure how it works - it uses starred expression and I don't really know what that is

def combinations(items):
    return (set(itertools.compress(items,mask)) for mask in itertools.product(*[[0,1]]*len(items)))

print('Compiling input components...')

vital_adapters = find_vital_adapters(puzzle_input)
nonvital_adapters = find_nonvital_adapters(puzzle_input, vital_adapters)

# find all permutations of nonvitals
nonvital_adapter_combinations = list(combinations(nonvital_adapters))

print('calculating...')

# start progress Bar
completion_bar = FancyBar(max=len(nonvital_adapter_combinations))

# set counter
counter = 0

# test all permutations
for test_set in nonvital_adapter_combinations:

    if check_adapter_sequence_validity(test_set.union(vital_adapters)):

        counter +=1

    completion_bar.next()

print(counter)
