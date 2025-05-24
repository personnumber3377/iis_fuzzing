
import random
MAX_SEED = 100_000
MAX_SUBSTRING_LENGTH = 30 # Use 30 as the maximum substring length
ABSOLUTE_MAX_OUTPUT = 4000 # Use 4k as absolute maximum output...


seed = random.randint(0, MAX_SEED)
print("Using this seed: "+str(seed))
random.seed(seed)
import string as string_mod # string.printable

MAX_REPEAT_COUNT = 5

HTTP_DICT_FILE = "http_dict.txt"

def load_dict() -> list: # Loads the strings from the dictionary as a list.
	fh = open(HTTP_DICT_FILE, "r")
	lines = fh.readlines() # Read all the lines...
	fh.close()
	# Now check the stuff thing...
	out_dict = []
	for line in lines:
		if len(line) <= 2 or line[0] == "#": # Check for comment...
			continue
		if line[-1] == "\n":
			line = line[:-1] # Cut out newline
		if line[0] == "\"" and line[-1] == "\"":
			out_dict.append(line[1:-1]) # Cut out double quotes...
		else:
			out_dict.append(line)
	out_dict = [x.encode() for x in out_dict]
	return out_dict

fuzzing_dictionary = load_dict()
print("Fuzzing dict: "+str(b"\n".join(fuzzing_dictionary)))
print("Dictionary length: "+str(len(fuzzing_dictionary)))

def add_dictionary_string(string: bytes) -> str:
	# Adds a dictionary string to "string"
	dict_entry = random.choice(fuzzing_dictionary)
	if not string:
		return dict_entry
	insert_index = random.randrange(max(len(string) - 1, 1))
	assert isinstance(dict_entry, bytes)
	assert isinstance(string, bytes)
	return string[:insert_index] + dict_entry + string[insert_index:]

def remove_substring(string: bytes) -> str:
	if not string:
		return string
	start_index = random.randrange(max(len(string)-1, 1))
	end_index = random.randrange(start_index, len(string))
	return string[:start_index] + string[end_index:]

def multiply_substring(string: bytes) -> str:
	if not string:
		return string
	if len(string) <= 2:
		return string * random.randrange(MAX_REPEAT_COUNT)
	start_index = random.randrange(max(len(string)-1, 1))
	# end_index = random.randrange(start_index, len(string))
	end_index = random.randrange(start_index, min(start_index + MAX_SUBSTRING_LENGTH, len(string) - 1))
	substr = string[start_index:end_index]
	where_to_place = random.randrange(max(len(string)-1, 1))
	return string[:where_to_place] + (substr * random.randrange(MAX_REPEAT_COUNT)) + string[where_to_place:]

def add_character(string: bytes) -> str:
	#if len(string)-1 >= 1:
	if not string:
		# print("oof")
		return bytes([random.randrange(0,256)])
	where_to_place = random.randrange(max(len(string)-1, 1))
	# print("oof")
	return string[:where_to_place] + bytes([random.randrange(0,256)]) + string[where_to_place:]


def actual_mutate(string: bytes) -> bytes:
	strat = random.randrange(4)

	match strat:
		case 0:
			# Remove substring
			return remove_substring(string)
		case 1:
			# Multiply substring.
			return multiply_substring(string)
		case 2:
			# Add a character somewhere
			return add_character(string)
		case 3:
			# Add dictionary string...
			return add_dictionary_string(string)
		case _:
			print("Invalid")
			assert False
	print("Invalid")
	assert False

def mutate_http(string: bytes) -> str: # Mutate a string.
	# print("we were passed this here: "+str(string))
	output = actual_mutate(string)
	# Now just cap it out at maximum thing...
	# print("Fuc")
	if len(output) >= ABSOLUTE_MAX_OUTPUT:
		output = output[:ABSOLUTE_MAX_OUTPUT]
	assert len(output) <= ABSOLUTE_MAX_OUTPUT
	return output # Return that shit...

