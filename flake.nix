{
description = "Flutter 3.13.x";
inputs = {
  nixpkgs.url = "github:NixOS/nixpkgs/23.11";
  flake-utils.url = "github:numtide/flake-utils";
};
outputs = { self, nixpkgs, flake-utils }:
  flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs {
        inherit system;
        config = {
          android_sdk.accept_license = true;
          allowUnfree = true;
        };
      };
      buildToolsVersion = "34.0.0";
      androidComposition = pkgs.androidenv.composeAndroidPackages {
        buildToolsVersions = [ buildToolsVersion ];
        platformVersions = [ "33" "34" "32" ];
        # abiVersions = [ "armeabi-v7a" "arm64-v8a" ];
      };
      androidSdk = androidComposition.androidsdk;
    in
    {
      devShell =
        with pkgs; mkShell rec {
          ANDROID_SDK_ROOT = "${androidSdk}/libexec/android-sdk";
          buildInputs = [
            flutter
            androidSdk
            jdk17

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
    });
}

