{
  description = "A Python development environment";

  inputs = { nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable"; };

  outputs = { self, nixpkgs }:
    let
      forAllSystems = function:
        nixpkgs.lib.genAttrs [ "x86_64-linux" ]
          (system: function nixpkgs.legacyPackages.${system});

      generalPackages = pkgs: with pkgs; [
        nodejs
        pre-commit
        rich-cli
        python311
        # vagrant
      ];

      pythonPackages = pkgs: with pkgs.python311Packages; [
        pip
        pip-tools
      ];
    in {
      devShells = forAllSystems (pkgs: {
        default = pkgs.mkShell {
          packages = (generalPackages pkgs) ++ (pythonPackages pkgs);

          shellHook = ''
          poetry install
          export PS1="(deploy-shell 🚀) $PS1"
          '';
        };
      });
    };
}
