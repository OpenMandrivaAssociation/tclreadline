%define major		2.1.0
%define libname		%mklibname %{name} %{major}
%define develname	%mklibname %{name} -d

Summary:	Tcl/Tk readline enhanced shells
Name:		tclreadline
Version:	2.1.0
Release:	%mkrel 13
URL:		http://tclreadline.sourceforge.net
Source0:	ftp://tclreadline.sourceforge.net/pub/tclreadline/%{name}-%{version}.tar.bz2
Patch0:		%{name}-interp-paths.patch
Patch1:		%{name}-amd64.patch
License:	BSD
Group:		Development/Other
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	readline-devel
BuildRequires:	ncurses-devel
BuildRequires:	X11-devel
BuildRequires:	tk
BuildRequires:	tk-devel
BuildRequires:	tcl
BuildRequires:	tcl-devel
BuildRequires:	autoconf

%description
This package contains tclreadline library, which builds a connection
between tcl and the gnu readline.

%package -n %{libname}
Group: System/Libraries
Summary: GNU readline for TCL
Provides: lib%{name} = %{version}

%description -n %{libname}
This package contains tclreadline library, which builds a connection
between tcl and the gnu readline.

%package -n %{develname}
Group:		Development/C
Summary:	Development headers and libraries
Requires:	%{libname} = %{version}
Provides:	lib%{name}-devel = %{version}
Provides:	%{name}-devel = %{version}
Obsoletes:	%{mklibname tclreadline 2.1.0 -d}

%description -n %{develname}
Development headers and libraries for tclreadline
 
%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
rm -f config/missing
%{__libtoolize} --force
autoreconf -i -I aux
%configure --enable-tclshrl --enable-wishrl
make

%install
rm -rf %{buildroot}
%makeinstall_std

%multiarch_includes %{buildroot}%{_includedir}/tclreadline.h
chmod 755 %{buildroot}%{_libdir}/tclreadline%{major}/{tclreadlineSetup.tcl,tclreadlineInit.tcl,pkgIndex.tcl}
chmod 644 %{buildroot}%{_libdir}/*.la

ln -sf libtclreadline-%{major}.so %{buildroot}%{_libdir}/libtclreadline.so.%{major}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%doc AUTHORS COPYING ChangeLog README TODO
%{_bindir}/tclshrl
%{_bindir}/wishrl

%files -n %{libname}
%{_libdir}/tclreadline%{major}
%{_libdir}/libtclreadline-%{major}.so
%{_libdir}/libtclreadline.so.*

%files -n %{develname}
%multiarch %{multiarch_includedir}/tclreadline.h
%{_includedir}/tclreadline.h
%{_libdir}/libtclreadline.a 
%{_libdir}/libtclreadline.la
%{_libdir}/libtclreadline.so
%{_mandir}/mann/tclreadline.n.*

