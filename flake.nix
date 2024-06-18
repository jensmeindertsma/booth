{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem
    (
      system: let
        overlays = [
          (final: prev: {
            pythonEnv = prev.python3.withPackages (ps: []);
          })
        ];
        pkgs = import nixpkgs {
          inherit system overlays;
        };
      in
        with pkgs; {
          devShells.default = mkShell {
            buildInputs = [
              pythonEnv
            ];
            shellHook = ''
              VENV=.venv
              if test ! -d $VENV; then
                python -m venv $VENV
              fi
              source ./$VENV/bin/activate
            '';
          };
        }
    );
}
