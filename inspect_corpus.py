import sys
import pickle

def main():
    if len(sys.argv) != 2:
        print("Usage: python load_list.py <filename.pkl>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        with open(filename, 'rb') as f:
            data = pickle.load(f)

        if isinstance(data, list):
            print("Loaded list:")
            print(data)
        else:
            print(f"The file does not contain a list. Found type: {type(data)}")

    except FileNotFoundError:
        print(f"File not found: {filename}")
    except pickle.UnpicklingError:
        print(f"Error unpickling file: {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()