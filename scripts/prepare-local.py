import yaml
import os
import sys

def main():
    values_path = "chart/values.yaml"
    output_dir = "local-dev/config"

    if not os.path.exists(values_path):
        print(f"Error: {values_path} not found.")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    with open(values_path, "r") as f:
        try:
            values = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(f"Error parsing values.yaml: {exc}")
            sys.exit(1)

    config = values.get("config", {})
    if not config:
        print("No 'config' section found in values.yaml")
        sys.exit(1)

    for filename, content in config.items():
        if filename == "allowedHosts":
            continue
        file_path = os.path.join(output_dir, filename)
        with open(file_path, "w") as f:
            f.write(content)
        print(f"Extracted {filename}")

    print("Configuration preparation complete.")

if __name__ == "__main__":
    main()
