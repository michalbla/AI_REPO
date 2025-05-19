class Directory:
    def __init__(self, name):
        self.name = name
        self.children = []

def new_directory(name):
    return Directory(name)

def add_directory(parent, name):
    if any(child.name == name for child in parent.children):
        print(f"Directory '{name}' already exists under '{parent.name}'.")
        return
    parent.children.append(new_directory(name))

def print_structure(root_dir, indent=0):
    if root_dir is None:
        return
    print("  " * indent + root_dir.name)
    for child in root_dir.children:
        print_structure(child, indent + 1)

def dfs_search_all_paths(root_dir, name, path="root", paths=None, nodes=None):
    if paths is None:
        paths = []
    if nodes is None:
        nodes = []

    print(f"Visiting node: {root_dir.name}")

    if root_dir.name == name:
        paths.append(path)
        nodes.append(root_dir)

    for child in root_dir.children:
        dfs_search_all_paths(child, name, f"{path}/{child.name}", paths, nodes)

    return paths, nodes

def bfs_search(root_dir, name):
    from collections import deque

    queue = deque([(root_dir, "root")])
    visited_paths = []

    while queue:
        current, path = queue.popleft()
        visited_paths.append(path)

        print(f"Visiting node: {current.name} (Path: {path})")

        if current.name == name:
            print(f"Found '{name}' at: '{path}'.")
            print("BFS visited paths:")
            for visited in visited_paths:
                print(f" - {visited}")
            return path

        for child in current.children:
            queue.append((child, f"{path}/{child.name}"))

    print(f"Directory not found: '{name}'.")
    print("BFS visited paths:")
    for visited in visited_paths:
        print(f" - {visited}")
    return None

def remove_directory_by_reference(parent, directory):
    if directory in parent.children:
        parent.children.remove(directory)
        return True
    return False

def remove_directory(root_dir, name):
    paths, nodes = dfs_search_all_paths(root_dir, name)

    if not nodes:
        print("Directory not found.")
        return False

    if len(nodes) == 1:
        node_to_remove = nodes[0]

        if node_to_remove in root_dir.children:
            root_dir.children.remove(node_to_remove)
            print(f"Removed directory '{name}' from root.")
            return True

        for parent in root_dir.children:
            if remove_directory_by_reference(parent, node_to_remove):
                print(f"Removed directory '{name}' from '{paths[0]}'.")
                return True
    else:
        print("Multiple directories found:")
        for i, path in enumerate(paths):
            print(f"{i + 1}. {path}")
        try:
            choice = int(input("Select the directory to remove by number: ")) - 1
            if 0 <= choice < len(nodes):
                node_to_remove = nodes[choice]

                if node_to_remove in root_dir.children:
                    root_dir.children.remove(node_to_remove)
                    print(f"Removed directory '{name}' from root.")
                    return True

                for parent in root_dir.children:
                    if remove_directory_by_reference(parent, node_to_remove):
                        print(f"Removed directory '{name}' from '{paths[choice]}'.")
                        return True
        except ValueError:
            print("Invalid selection. Please enter a number.")
            return False

    print("Failed to remove directory.")
    return False

def add_directory_logic(parent, name):
    if parent_name == "root":
        add_directory(root, dir_name)
    else:
        paths, nodes = dfs_search_all_paths(root, parent_name)
        if nodes:
            add_directory(nodes[0], dir_name)
            print(f"Added directory '{dir_name}' to '{paths[0]}'.")
        else:
            return

def search_directory(name):
    paths, _ = dfs_search_all_paths(root, name)
    if paths:
        print(f"Directory '{name}' found:")
        for path in paths:
            print(f" - {path}")
    else:
        print("Directory not found.")

if __name__ == '__main__':
    root = new_directory("root")
    while True:
        print("\nOptions:")
        print("1. Add directory")
        print("2. Remove directory")
        print("3. Search directory (DFS)")
        print("4. Search directory (BFS)")
        print("5. Print structure")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            parent_name = input("Enter parent directory name (or 'root' to add to root): ")
            dir_name = input("Enter new directory name: ")
            add_directory_logic(parent_name, dir_name)
        elif choice == "2":
            dir_name = input("Enter directory name to remove: ")
            remove_directory(root, dir_name)
        elif choice == "3":
            dir_name = input("Enter directory name to search: ")
            search_directory(dir_name)
        elif choice == "4":
            dir_name = input("Enter directory name to search: ")
            bfs_search(root, dir_name)
        elif choice == "5":
            print("Directory structure:")
            print_structure(root)
        elif choice == "6":
            break
        else:
            print("Invalid option. Please try again.")

