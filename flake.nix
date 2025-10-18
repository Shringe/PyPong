{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/release-25.05";
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
        pkgs = import nixpkgs {
          inherit system;
        };
      in
      with pkgs;
      {
        packages.default = pkgs.python3Packages.buildPythonPackage rec {
          pname = "pypong";
          version = "alpha";
          src = self;
          pyproject = false;
          dontUnpack = true;

          installPhase = ''
            install -Dm755 "${./PyPongALPHA.py}" "$out/bin/${pname}"
          '';

          propagatedBuildInputs = with pkgs.python3Packages; [
            pygame
          ];
        };

        devShells.default = mkShell {
          buildInputs = with pkgs; [
            python3
            python3Packages.pygame
          ];

          shellHook = ''
            echo "Hello! Welcome to the PyPong development shell. Start the game with: python3 \"./PyPongALPHA.py\""
          '';
        };
      }
    );
}
