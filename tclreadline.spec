%define _disable_ld_no_undefined	1

Summary:	Tcl/Tk readline enhanced shells
Name:		tclreadline
Version:	2.1.0
Release:	%mkrel 17
URL:		http://tclreadline.sourceforge.net
Source0:	ftp://tclreadline.sourceforge.net/pub/tclreadline/%{name}-%{version}.tar.bz2
Patch1:		%{name}-amd64.patch
# upstream assumes tkConfig.sh and tclConfig.sh are always in the same
# directory, which isn't the case for us now - AdamW 2008/10
Patch2:		tclreadline-2.1.0-tk.patch
# installs everything to whatever's set as libdir - so we can just
# install the whole thing to tcl_sitearch/name (see below) - AdamW
# 2008/10
Patch3:		tclreadline-2.1.0-tcl_relocate.patch
License:	BSD
Group:		Development/Other
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	readline-devel
BuildRequires:	ncurses-devel
BuildRequires:	X11-devel
BuildRequires:	tk
BuildRequires:	tk-devel
BuildRequires:	tcl
BuildRequires:	tcl-devel
BuildRequires:	autoconf
Obsoletes:	%{mklibname tclreadline -d} < %{version}-%{release}
Obsoletes:	%{mklibname tclreadline 2.1.0 -d} < %{version}-%{release}

%description
This package contains tclreadline, a TCL package which builds a
connection between TCL and the GNU readline.

%prep
%setup -q
%patch2 -p1
%patch1 -p1
%patch3 -p1

# fix interpreter path
perl -pi -e 's|^#!/usr/local/bin/tclsh|#!/usr/bin/tclsh|' \
    tclreadlineInit.tcl.in \
    tclreadlineSetup.tcl.in \
    pkgIndex.tcl.in

%build
rm -f config/missing
%{__libtoolize} --force
autoreconf -i -I aux
%configure2_5x --enable-tclshrl --enable-wishrl --libdir=%{tcl_sitearch}/%{name}%{version}
make

%install
rm -rf %{buildroot}
%makeinstall_std

# remove unneeded crap - it's not really a shared library and nothing
# is ever going to build against it - AdamW 2008/10
rm -f %{buildroot}%{tcl_sitearch}/%{name}%{version}/*.*a
rm -rf %{buildroot}%{_includedir}


%clean
rm -rf %{buildroot}

%files
%doc AUTHORS COPYING ChangeLog README TODO
%{_bindir}/tclshrl
%{_bindir}/wishrl
%{tcl_sitearch}/%{name}%{version}
%{_mandir}/mann/tclreadline.n.*
