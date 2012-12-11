Summary:	Tcl/Tk readline enhanced shells
Name:		tclreadline
Version:	2.1.0
Release:	%mkrel 19
URL:		http://tclreadline.sourceforge.net
Source0:	ftp://tclreadline.sourceforge.net/pub/tclreadline/%{name}-%{version}.tar.bz2
Patch0:		tclreadline-2.1.0-link.patch
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
%patch0 -p0
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
autoreconf -i --force -I aux
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


%changelog
* Tue Feb 01 2011 Funda Wang <fwang@mandriva.org> 2.1.0-19mdv2011.0
+ Revision: 634685
- fix linkage

* Sun Sep 20 2009 Thierry Vignaud <tv@mandriva.org> 2.1.0-18mdv2010.0
+ Revision: 445378
- rebuild

* Fri Feb 27 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.1.0-17mdv2009.1
+ Revision: 345415
- use autoreconf --force flag to update files
- don't run libtoolize twice
- build for new readline
- use substitution rather than patches for fixing interpreter path
- switch remaining patches order

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild for new libreadline

* Fri Dec 05 2008 Adam Williamson <awilliamson@mandriva.org> 2.1.0-15mdv2009.1
+ Revision: 310155
- rebuild for new tcl
- drop all the development header stuff, not needed
- move to new location per policy
- drop the libification crap, tcl modules are not shared libraries
- add tcl_relocate.patch to allow installation to new location per policy
- add tk.patch: allows tclConfig.sh and tkConfig.sh to be in different places
- use ld_no_undefined (won't build without, no shared lib)

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - rebuild
    - fix no-buildroot-tag

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sat Jan 12 2008 Adam Williamson <awilliamson@mandriva.org> 2.1.0-11mdv2008.1
+ Revision: 149667
- remove now unneeded BR on automake1.4
- rebuild for new tcl/tk
- use %%__libtoolize --force to avoid build breakage related to hilariously old libtool-related files
- use autoreconf
- spec clean, remove lots of old garbage

  + Thierry Vignaud <tv@mandriva.org>
    - kill XFree86-libs BR
    - kill re-definition of %%buildroot on Pixel's request
    - fix autoconf-2.5x path
    - buildrequires X11-devel instead of XFree86-devel


* Mon Jan 02 2006 Oden Eriksson <oeriksson@mandriva.com> 2.1.0-10mdk
- rebuilt against soname aware deps (tcl/tk)
- fix deps

* Fri Jul 29 2005 Nicolas Lécureuil <neoclust@mandriva.org> 2.1.0-9mdk
- Fix BuildRequires

* Sat Jul 23 2005 Couriousous <couriousous@mandriva.org> 2.1.0-8mdk
- Fix spec
- Amd64 patch from pld
- From Torbjorn Turpeinen <tobbe@nyvalls.se> 
	- Built for cooker

