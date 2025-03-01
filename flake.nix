{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };
      in
      with pkgs;
      {
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
