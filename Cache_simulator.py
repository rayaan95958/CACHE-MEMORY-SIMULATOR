def create_cache_block(tag=-1, valid_bit=False, lru_counter=0):
    return
    {
        "tag": tag,
        "valid_bit": valid_bit,
        "lru_counter": lru_counter
    }

def create_cache_set(associativity):
    return [create_cache_block() for _ in range(associativity)]

def cache(cache_size, block_size, mapping_strategy):
    try:
        if mapping_strategy == 1:
            associativity = 1
            num_sets = cache_size // block_size
        elif mapping_strategy == 2:
            associativity = cache_size // block_size
            num_sets = 1
        elif mapping_strategy == 3:
            associativity = 2
            num_sets = cache_size // (block_size * associativity)
        else:
            raise ValueError("Invalid mapping strategy. Choose from 1 (Direct), 2 (Associative), or 3 (2-Way Set Associative).")
        
        sets = [create_cache_set(associativity) for _ in range(num_sets)]
        return {
            "cache_size": cache_size,
            "block_size": block_size,
            "mapping_strategy": mapping_strategy,
            "associativity": associativity,
            "num_sets": num_sets,
            "sets": sets
        }
    except ZeroDivisionError:
        print("Error: Block size cannot be zero.")
        return None
    except ValueError as e:
        print(f"Error: {e}")
        return None

def access_cache(cache, address):
    try:
        index_bits = len(bin(cache["num_sets"] - 1)[2:])
        offset_bits = len(bin(cache["block_size"] - 1)[2:])
        tag_bits = 16 - index_bits - offset_bits

        tag = (address >> (index_bits + offset_bits)) & ((1 << tag_bits) - 1)
        index = (address >> offset_bits) % cache["num_sets"]

        set_blocks = cache["sets"][index]
        hit = False
        max_lru_counter = max(block["lru_counter"] for block in set_blocks)
        lru_block_index = min(range(cache["associativity"]), key=lambda i: set_blocks[i]["lru_counter"])
        
        for block in set_blocks:
            if block["valid_bit"] and block["tag"] == tag:
                hit = True
                block["lru_counter"] = max_lru_counter + 1
                return True, False, None

        eviction = set_blocks[lru_block_index]["valid_bit"]
        set_blocks[lru_block_index]["tag"] = tag
        set_blocks[lru_block_index]["valid_bit"] = True
        set_blocks[lru_block_index]["lru_counter"] = max_lru_counter + 1

        return False, True, eviction
    except (IndexError, KeyError):
        print("Error: Cache access out of bounds.")
        return False, False, None

def simulate_cache(cache, memory_trace):
    hits = 0
    misses = 0
    evictions = 0
    total_accesses = 0
    for address in memory_trace:
        total_accesses += 1
        hit, miss, eviction = access_cache(cache, address)
        if hit:
            hits += 1
        if miss:
            misses += 1
        if eviction:
            evictions += 1
    return hits, misses, evictions, total_accesses

def display_results(hits, misses, evictions, total_accesses):
    # Display the results of the cache simulation
    print("Hits:", hits)
    print("Misses:", misses)
    print("Hit rate:", hits / total_accesses)
    print("Miss rate:", misses / total_accesses)

def main():
    try:
        print("......Single Level Cache Simulator......")
        print("Assuming main memory address is 16 bit wide")
        cache_size = int(input("Enter the capacity of the cache memory in bytes: "))
        block_size = int(input("Enter the block size in bytes: "))
        print("Choose the mapping strategy:")
        print("1: Direct Mapping")
        print("2: Associative Mapping")
        print("3: 2-Way Set Associative")
        mapping_strategy = int(input("Enter the mapping strategy (1, 2, 3): "))

        memory_trace = []
        while True:
            address = input("Enter memory address in hexadecimal (enter 'done' to finish): ")
            if address.lower() == 'done':
                break
            else:
                try:
                    int_address = int(address, 16)
                    if 0 <= int_address <= 0xFFFF:
                        memory_trace.append(int_address)
                    else:
                        print("Invalid memory address. Please enter a valid 16-bit hexadecimal address.")
                except ValueError:
                    print("Invalid input. Please enter a valid 16-bit hexadecimal address.")

        cache_obj = cache(cache_size, block_size, mapping_strategy)
        if cache_obj is not None:
            hits, misses, evictions, total_accesses = simulate_cache(cache_obj, memory_trace)
            display_results(hits, misses, evictions, total_accesses)
    except ValueError:
        print("Error: Please provide valid input.")

if __name__ == "__main__":
    main()