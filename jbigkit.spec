%define	name	jbigkit
%define	version	1.5
%define	rel	5

Name:		%{name}
Summary:	The JBIG Kit
Version:	%{version}
Release:	%mkrel %{rel}
License:	GPL
Source0:	http://www.cl.cam.ac.uk/~mgk25/download/jbigkit-1.5.tar.bz2
Patch0:		jbigkit-1.6.patch
URL:		http://www.cl.cam.ac.uk/~mgk25
Group:		Graphics
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
JBIG is a highly effective lossless compression algorithm for bi-level
images (one bit per pixel), which is particularly suitable for scanned
document pages.

%package -n libjbig-devel
Summary:  Header files and static library for development with JBIG
Group: Development/C
%description -n libjbig-devel
This package is only needed if you plan to develop or compile
applications which requires the libjbig library.

%prep
%setup -q -n %{name}
%patch0 -p1 -b .16

%build
make CCFLAGS="$RPM_OPT_FLAGS -fPIC -DPIC"
make test
mv -f libjbig/jbig.doc libjbig/jbig.txt

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir} \
    $RPM_BUILD_ROOT%{_includedir} \
    $RPM_BUILD_ROOT%{_libdir} \
    $RPM_BUILD_ROOT%{_mandir}/man1
#
install pbmtools/jbgtopbm $RPM_BUILD_ROOT%{_bindir}
install pbmtools/pbmtojbg $RPM_BUILD_ROOT%{_bindir}
install pbmtools/jbgtopbm.1 $RPM_BUILD_ROOT%{_mandir}/man1
install pbmtools/pbmtojbg.1 $RPM_BUILD_ROOT%{_mandir}/man1
install libjbig/libjbig.a $RPM_BUILD_ROOT%{_libdir}
install libjbig/jbig.h $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc ANNOUNCE COPYING INSTALL TODO
%attr(755,root,root) %{_bindir}/*
%attr(644,root,root) %{_mandir}/man1/*

%files -n libjbig-devel
%defattr(-,root,root)
%doc ANNOUNCE COPYING INSTALL TODO libjbig/jbig.txt
%attr(644,root,root) %{_includedir}/*.h
%{_libdir}/*.a


