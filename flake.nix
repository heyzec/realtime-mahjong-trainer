{
  description = "Template for a direnv shell, with Python";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
  let 
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};

  in
  {
    devShells.${system}.default = pkgs.mkShell {
      buildInputs = with pkgs; [
        (let
          python-packages = ps: with ps; [
            (buildPythonPackage rec {
            pname = "mahjong";
              version = "1.2.1";
              src = fetchPypi {
                inherit pname version;
                sha256 = "r77y9f6mVrc+rLY5YXbR6AzQYSPCTb6iffhxAOhQIJc=";
              };
              doCheck = false;
              propagatedBuildInputs = [
                # # Specify dependencies
                # pkgs.python3Packages.numpy
              ];
            })
          ];
        in python3.withPackages python-packages)
      ];
    };
  };
}

