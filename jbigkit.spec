%define	major 0
%define libname %mklibname jbig %{major}
%define develname %mklibname jbig -d

Summary:	The JBIG-KIT
Name:		jbigkit
Version:	1.6
Release:	%mkrel 4
License:	GPL
Group:		Graphics
URL:		http://www.cl.cam.ac.uk/~mgk25
Source0:	http://www.cl.cam.ac.uk/~mgk25/download/%{name}-%{version}.tar.gz
Patch0:		jbigkit-1.6-build.patch
Patch1:		jbigkit-1.6-respect-make.patch
Patch2:		jbigkit-shared.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
JBIG-KIT implements a highly effective data compression algorithm for bi-level
high-resolution images such as fax pages or scanned documents.

%package -n	%{libname}
Summary:	The Shared library for The JBIG-KIT
Group:          System/Libraries

%description -n	%{libname}
JBIG-KIT implements a highly effective data compression algorithm for bi-level
high-resolution images such as fax pages or scanned documents.

This package provides the shared JBIG-KIT library.

%package -n	%{develname}
Summary:	Static library and header files for development with JBIG-KIT
Group:		Development/C
Requires:	%{libname} = %{version}
%if "%{_lib}" == "lib64"
Provides:	libjbig-devel = %{version}-%{release}
Obsoletes:	libjbig-devel
%endif
Provides:	jbig-devel = %{version}-%{release}
Obsoletes:	jbig-devel
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel

%description -n	%{develname}
JBIG-KIT implements a highly effective data compression algorithm for bi-level
high-resolution images such as fax pages or scanned documents.

This package is only needed if you plan to develop or compile applications
which requires the libjbig library.

%prep

%setup -q -n %{name}

# fix strange perms
find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
export LDFLAGS="`rpm --eval %%configure|grep LDFLAGS|cut -d\\" -f2|sed -e 's/\$LDFLAGS\ //'`"
make CFLAGS="%{optflags} -fPIC -DPIC -I../libjbig" LDFLAGS="$LDFLAGS"

make test

mv -f libjbig/jbig.doc libjbig/jbig.txt

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_includedir}
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_mandir}/man5

install -m0755 pbmtools/jbgtopbm %{buildroot}%{_bindir}/
install -m0755 pbmtools/pbmtojbg %{buildroot}%{_bindir}/

install -m0644 pbmtools/*.1 %{buildroot}%{_mandir}/man1/
install -m0644 pbmtools/*.5 %{buildroot}%{_mandir}/man5/

install -m0755 libjbig/libjbig.so.0.0 %{buildroot}%{_libdir}/libjbig.so.0.0
ln -snf libjbig.so.0.0 %{buildroot}%{_libdir}/libjbig.so.0
ln -snf libjbig.so.0.0 %{buildroot}%{_libdir}/libjbig.so

install -m0644 libjbig/libjbig.a %{buildroot}%{_libdir}
install -m0644 libjbig/jbig.h %{buildroot}%{_includedir}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/*
%attr(0644,root,root) %{_mandir}/man1/*
%attr(0644,root,root) %{_mandir}/man5/*

%files -n %{libname}
%defattr(-,root,root)
%doc ANNOUNCE CHANGES COPYING
%attr(0755,root,root) %{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%doc  INSTALL TODO libjbig/jbig.txt
%attr(0644,root,root) %{_includedir}/*.h
%attr(0644,root,root) %{_libdir}/*.so
%attr(0644,root,root) %{_libdir}/*.a
