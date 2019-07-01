%define major	2
%define libname	%mklibname jbig %{major}
%define lib85	%mklibname jbig 85 %{major}
%define devname	%mklibname jbig -d

Summary:	The JBIG-KIT
Name:		jbigkit
Version:	2.1
Release:	1
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

%prep
%autosetup -p1

# fix strange perms
find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

%build
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
