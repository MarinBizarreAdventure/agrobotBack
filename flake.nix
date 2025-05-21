# flake.nix
{
  description = "Development environment for the Python Monolith Exam App";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable"; # Or a specific NixOS release branch like "nixos-23.11"
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        # --- Customizable Settings ---
        pythonVersion = "python312"; # Choose your desired Python version (e.g., python310, python311, python312)
        projectName = "agrobot";

        # --- System Packages ---
        pkgs = nixpkgs.legacyPackages.${system};

        # List system dependencies needed by your Python packages or tools
        # Examples:
        # - libpq for psycopg2 (PostgreSQL driver)
        # - openssl, zlib for various packages
        # - build tools
        systemDeps = with pkgs; [
          # Core build tools
          pkg-config
          gcc
          gcc.cc.lib
          zlib

          # Example: If you use PostgreSQL
          postgresql.lib # Provides libpq.so

          # Example: If you need other common libs
          # openssl
          # zlib
          # sqlite

        ];

        # Python interpreter and Poetry
        pythonEnv = pkgs.${pythonVersion};
        poetry = pkgs.poetry;

      in
      {
        # --- Development Shell ---
        # Access with `nix develop`
        devShells.default = pkgs.mkShell {
          name = "${projectName}-env";

          # Packages available in the shell
          packages = [
            pythonEnv # Provides the `python` command
            poetry # Provides the `poetry` command
          ] ++ systemDeps;

          # Environment variables and commands to run when entering the shell
          shellHook = ''
            echo "Entering ${projectName} development environment..."

            # Recommended: Configure Poetry to create the virtualenv inside the project directory (.venv)
            # This makes it easier for IDEs and tools to find it.
            export POETRY_VIRTUALENVS_IN_PROJECT=true
            export LD_LIBRARY_PATH="${pkgs.gcc.cc.lib}/lib:${pkgs.zlib}/lib:$LD_LIBRARY_PATH"


            # Optional: Automatically run 'poetry install' if needed
            # This checks if the venv exists and if poetry.lock is newer than the venv marker.
            # Remove or comment this out if you prefer running 'poetry install' manually.
            # Note: This might run 'poetry install' more often than strictly necessary on minor changes,
            # but ensures consistency when entering the shell.
            if [ ! -d ".venv" ] || [ "poetry.lock" -nt ".venv" ]; then
              echo "Running 'poetry install --sync' to set up/update virtual environment..."
              # --sync removes packages not in the lock file - good for consistency
              # --no-root prevents installing the project itself in editable mode into the venv,
              # which is often the desired behavior for applications.
              poetry install --sync --no-root
            else
              echo "Poetry virtual environment (.venv) seems up-to-date."
            fi

            # You can add other exports here if needed
            # export DATABASE_URL="postgresql://user:pass@host:port/db"

            echo "Ready! Use 'poetry run ...' or activate with 'poetry shell'."
          '';
        };

        # --- Optional: Packaging (More Advanced) ---
        # If you wanted Nix to build your *entire* application package (using tools like poetry2nix)
        # you would define it here in `packages.default`. This is more complex than just
        # using the devShell for running/developing with Poetry directly.
        # For typical monolith deployment, you often deploy the source + venv,
        # so the devShell is usually the main focus of the flake.

      }
    );
}
