
%define name tclreadline
%define version 2.1.0

%define rel 10

%{?!mkrel:%define mkrel(c:) %{-c: 0.%{-c*}.}%{!?_with_unstable:%(perl -e '$_="%{1}";m/(.\*\\D\+)?(\\d+)$/;$rel=${2}-1;re;print "$1$rel";').%{?subrel:%subrel}%{!?subrel:1}.%{?distversion:%distversion}%{?!distversion:%(echo $[%{mdkversion}/10])}}%{?_with_unstable:%{1}}%{?distsuffix:%distsuffix}%{?!distsuffix:mdk}}

%define release %mkrel %rel

%define major 2.1.0
%define libname %mklibname %{name} %major

Summary: Tcl/Tk readline enhanced shells
Name: %{name}
Version: %{version}
Release: %{release}
URL: http://tclreadline.sourceforge.net
Source0: ftp://tclreadline.sourceforge.net/pub/tclreadline/%{name}-%{version}.tar.bz2
Patch0:  %{name}-interp-paths.patch
Patch1:	 %{name}-amd64.patch
License: BSD
Group: Development/Other
BuildRequires: readline-devel ncurses-devel tcl X11-devel
BuildRequires: tk tk-devel tcl tcl-devel
BuildRequires:  autoconf2.5
BuildRequires:  automake1.4

%package -n %{libname}
Group: System/Libraries
Summary: GNU readline for TCL
Provides: lib%{name} = %{version}

%package -n %{libname}-devel
Group: Development/C
Summary: Development headers and libraries
Requires: %{libname} = %{version}
Provides: lib%{name}-devel = %{version}

%description
Tclshrl and wishrl is readline enhanced replacement for tclsh and wish

%description -n %{libname}
This package contains tclreadline library, which builds a connection
between tcl and the gnu readline.

%description -n %{libname}-devel
Development headers and libraries for tclreadline
 
%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
export FORCE_AUTOCONF_2_5=1
rm -f config/missing
%{__libtoolize}
aclocal-1.4 -I aux
autoconf
automake-1.4
%configure --enable-tclshrl --enable-wishrl
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

%multiarch_includes $RPM_BUILD_ROOT%{_includedir}/tclreadline.h
chmod 755 $RPM_BUILD_ROOT%{_libdir}/tclreadline%major/{tclreadlineSetup.tcl,tclreadlineInit.tcl,pkgIndex.tcl}
chmod 644 $RPM_BUILD_ROOT%{_libdir}/*.la

ln -sf libtclreadline-%{major}.so $RPM_BUILD_ROOT%{_libdir}/libtclreadline.so.%major

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc AUTHORS COPYING ChangeLog README TODO
%{_bindir}/tclshrl
%{_bindir}/wishrl

%files -n %{libname}
%{_libdir}/tclreadline%major
%{_libdir}/libtclreadline-%major.so
%{_libdir}/libtclreadline.so.*

%files -n %{libname}-devel
%multiarch %{multiarch_includedir}/tclreadline.h
%{_includedir}/tclreadline.h
%{_libdir}/libtclreadline.a 
%{_libdir}/libtclreadline.la
%{_libdir}/libtclreadline.so
%{_mandir}/mann/tclreadline.n.*

