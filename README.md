## About

*Conan recipe for [QuaZIP (LGPL-2.1)](https://github.com/stachenov/quazip)*

QuaZIP is a C++ wrapper for Gilles Vollant's ZIP/UNZIP package (AKA Minizip) using Qt library.

The recipe doesn't depend on zlib from Qt: it will install zlib as its dependency.

The recipe will install Qt5 as its dependency, so it doesn't rely on any existing Qt5 installation.

Example:
```
conan create <path-to-recipe> <username>/<channel>
```
