{
  description = "Xcel TOU Calculator - Python/Jupyter environment for electrical billing calculations";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python311
            uv
            git
          ];

          shellHook = ''
            echo "🔋 Xcel TOU Calculator Development Environment"
            echo "Python: $(python --version)"
            echo "UV: $(uv --version)"
            echo ""
            echo "Getting started:"
            echo "  uv sync - Install dependencies"
            echo "  uv run jupyter notebook - Start Jupyter notebook server"
            echo "  uv add <package> - Add Python dependencies"
            echo ""
          '';
        };
      });
}