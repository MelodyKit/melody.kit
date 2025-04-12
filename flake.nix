{
  description = "MelodyKit core";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    overlay.url = "github:oxalica/rust-overlay";
    utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      overlay,
      utils,
      ...
    }:
    utils.lib.eachSystem utils.lib.allSystems (
      system:
      let
        overlays = [ (import overlay) ];

        pkgs = import nixpkgs {
          inherit system overlays;
        };
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            (rust-bin.fromRustupToolchainFile (self + "/rust-toolchain.toml"))
          ];
        };
      }
    );
}
