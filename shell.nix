with import <nixpkgs> { };
with pkgs.python3Packages;

#let
  #theme = buildPythonPackage rec {
    #name = "mkdocs-gitbook";
    #src = fetchFromGitLab {
      #owner = "lramage";
      #repo = "mkdocs-gitbook-theme";
      #rev = "6e86220e";
      #sha256 = "1kq3j3vbr0xm8wg2jj4lri66g0v3bdsqzdpgpkdyl54mq4hnpxxv";
    #};
  #};
#in
pkgs.mkShell { buildInputs = [ rich hypothesis pytest mypy pylint click bottle black pynws ]; }
