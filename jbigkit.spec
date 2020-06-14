# jbigkit is used by ghostscript, ghostscript is used by libspectre,
# libspectre is used by cairo, cairo is used by gtk-3.0, gtk-3.0
# is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%endif

%define major	2
%define libname	%mklibname jbig %{major}
%define lib85	%mklibname jbig 85 %{major}
%define devname	%mklibname jbig -d

%define lib32name	%mklib32name jbig %{major}
%define lib3285	%mklib32name jbig 85 %{major}
%define dev32name	%mklib32name jbig -d

Summary:	The JBIG-KIT
Name:		jbigkit
Version:	2.1
Release:	2
License:	GPLv2
Group:		Graphics
Url:		http://www.cl.cam.ac.uk/~mgk25/jbigkit/
Source0:	http://www.cl.cam.ac.uk/~mgk25/download/%{name}-%{version}.tar.gz
BuildRequires:	libtool

Patch0:         jbigkit-2.1-shlib.patch
Patch1:         jbigkit-2.0-warnings.patch
Patch2:         jbigkit-ldflags.patch
# patch for coverity issues - backported from upstream
Patch3:         jbigkit-covscan.patch

%description
JBIG-KIT implements a highly effective data compression algorithm for bi-level
high-resolution images such as fax pages or scanned documents.

%package -n	%{libname}
Summary:	The Shared library for The JBIG-KIT
Group:		System/Libraries

%description -n	%{libname}
This package provides the shared JBIG-KIT library.

%package -n	%{lib85}
Summary:	The Shared library for The JBIG-KIT
Group:		System/Libraries
Conflicts:	%{_lib}jbig1 < 2.0-10

%description -n	%{lib85}
This package provides the shared JBIG-KIT library.

%package -n	%{devname}
Summary:	Development library and header files for development with JBIG-KIT
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{lib85} = %{version}-%{release}
Provides:	jbig-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
This package is only needed if you plan to develop or compile applications
which requires the libjbig library.

%if %{with compat32}
%package -n	%{lib32name}
Summary:	The Shared library for The JBIG-KIT (32-bit)
Group:		System/Libraries

%description -n	%{lib32name}
This package provides the shared JBIG-KIT library.

%package -n	%{lib3285}
Summary:	The Shared library for The JBIG-KIT (32-bit)
Group:		System/Libraries

%description -n	%{lib3285}
This package provides the shared JBIG-KIT library.

%package -n	%{dev32name}
Summary:	Development library and header files for development with JBIG-KIT (32-bit)
Group:		Development/C
Requires:	%{devname} = %{EVRD}
Requires:	%{lib32name} = %{version}-%{release}
Requires:	%{lib3285} = %{version}-%{release}

%description -n	%{dev32name}
This package is only needed if you plan to develop or compile applications
which requires the libjbig library.
%endif

%prep
%autosetup -p1

# fix strange perms
find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

%build
%if %{with compat32}
%make_build \
	CC="gcc -m32" \
	CFLAGS="%(echo %{optflags} |sed -e 's,-m64,,;s,-flto,,g') -m32 -fPIC -DPIC" \
	LDFLAGS="%(echo %{ldflags} |sed -e 's,-m64,,;s,-flto,,g') -m32" \
	prefix=%{_prefix} \
	libdir=%{_libdir}

mkdir lib32
mv libjbig/*.so* lib32
make clean
%endif

%make_build \
	CC=%{__cc} \
	CFLAGS="%{optflags} -fPIC -DPIC" \
	LDFLAGS="%{ldflags}" \
	prefix=%{_prefix} \
	libdir=%{_libdir}

%check
make test

%install
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
%if %{with compat32}
mkdir -p %{buildroot}%{_prefix}/lib
install -p -m0755 lib32/libjbig.so.%{version} $RPM_BUILD_ROOT/%{_prefix}/lib
install -p -m0755 lib32/libjbig85.so.%{version} $RPM_BUILD_ROOT/%{_prefix}/lib
ln -sf libjbig.so.%{version} $RPM_BUILD_ROOT/%{_prefix}/lib/libjbig.so
ln -sf libjbig85.so.%{version} $RPM_BUILD_ROOT/%{_prefix}/lib/libjbig85.so
%endif

install -p -m0755 libjbig/libjbig.so.%{version} $RPM_BUILD_ROOT/%{_libdir}
install -p -m0755 libjbig/libjbig85.so.%{version} $RPM_BUILD_ROOT/%{_libdir}
ln -sf libjbig.so.%{version} $RPM_BUILD_ROOT/%{_libdir}/libjbig.so
ln -sf libjbig85.so.%{version} $RPM_BUILD_ROOT/%{_libdir}/libjbig85.so

install -p -m0644 libjbig/jbig.h $RPM_BUILD_ROOT%{_includedir}
install -p -m0644 libjbig/jbig85.h $RPM_BUILD_ROOT%{_includedir}
install -p -m0644 libjbig/jbig_ar.h $RPM_BUILD_ROOT%{_includedir}

install -p -m0755 pbmtools/???to??? $RPM_BUILD_ROOT%{_bindir}
install -p -m0755 pbmtools/???to???85 $RPM_BUILD_ROOT%{_bindir}
install -p -m0644 pbmtools/*.1 $RPM_BUILD_ROOT%{_mandir}/man1
# cleanup
rm -f %{buildroot}%{_libdir}/*.a

%files
%doc ANNOUNCE CHANGES COPYING
%{_bindir}/*
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/libjbig.so.%{major}*

%files -n %{lib85}
%{_libdir}/libjbig85.so.%{major}*

%files -n %{devname}
%doc INSTALL TODO pbmtools/*.txt libjbig/*.txt
%{_includedir}/*.h
%{_libdir}/*.so

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libjbig.so.%{major}*

%files -n %{lib3285}
%{_prefix}/lib/libjbig85.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/*.so
%endif
