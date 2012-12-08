%define major 1
%define libname %mklibname jbig %{major}
%define develname %mklibname jbig -d

Summary:	The JBIG-KIT
Name:		jbigkit
Version:	2.0
Release:	9
License:	GPL
Group:		Graphics
URL:		http://www.cl.cam.ac.uk/~mgk25/jbigkit/
Source0:	http://www.cl.cam.ac.uk/~mgk25/download/%{name}-%{version}.tar.gz
Patch0:		jbigkit-2.0-shared.diff
BuildRequires:	libtool

%description
JBIG-KIT implements a highly effective data compression algorithm for bi-level
high-resolution images such as fax pages or scanned documents.

%package -n	%{libname}
Summary:	The Shared library for The JBIG-KIT
Group:		System/Libraries

%description -n	%{libname}
JBIG-KIT implements a highly effective data compression algorithm for bi-level
high-resolution images such as fax pages or scanned documents.

This package provides the shared JBIG-KIT library.

%package -n	%{develname}
Summary:	Static library and header files for development with JBIG-KIT
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	jbig-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

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

%build
make CFLAGS="%{optflags} -fPIC -DPIC" \
    LDFLAGS="%{ldflags}" prefix=%{_prefix} libdir=%{_libdir}

%check
make test

%install
rm -rf %{buildroot}

%makeinstall_std prefix=%{_prefix} libdir=%{_libdir}

# cleanup
rm -f %{buildroot}%{_libdir}/*.a

%files
%attr(0755,root,root) %{_bindir}/*
%attr(0644,root,root) %{_mandir}/man1/*
%attr(0644,root,root) %{_mandir}/man5/*

%files -n %{libname}
%doc ANNOUNCE CHANGES COPYING
%attr(0755,root,root) %{_libdir}/*.so.%{major}*

%files -n %{develname}
%doc INSTALL TODO pbmtools/*.txt libjbig/*.txt
%attr(0644,root,root) %{_includedir}/*.h
%attr(0644,root,root) %{_libdir}/*.so


%changelog
* Sat Dec 03 2011 Oden Eriksson <oeriksson@mandriva.com> 2.0-7
+ Revision: 737417
- drop the static lib and the libtool *.la file
- various fixes

* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 2.0-6
+ Revision: 665821
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 2.0-5mdv2011.0
+ Revision: 606077
- rebuild

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 2.0-4mdv2010.1
+ Revision: 519825
- rebuild

  + Funda Wang <fwang@mandriva.org>
    - update url

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 2.0-3mdv2010.0
+ Revision: 425454
- rebuild

* Sat Jan 31 2009 Oden Eriksson <oeriksson@mandriva.com> 2.0-2mdv2009.1
+ Revision: 335857
- add missing headers

* Sat Jan 31 2009 Oden Eriksson <oeriksson@mandriva.com> 2.0-1mdv2009.1
+ Revision: 335817
- 2.0
- rework the shared patch to use libtool
- new major 1

* Sat Dec 20 2008 Oden Eriksson <oeriksson@mandriva.com> 1.6-5mdv2009.1
+ Revision: 316438
- use the %%ldflags macro

* Fri Dec 19 2008 Oden Eriksson <oeriksson@mandriva.com> 1.6-4mdv2009.1
+ Revision: 316220
- use LDFLAGS from the %%configure macro

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 1.6-3mdv2009.0
+ Revision: 221709
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sun Jan 13 2008 Thierry Vignaud <tv@mandriva.org> 1.6-2mdv2008.1
+ Revision: 150418
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Sun Aug 12 2007 Oden Eriksson <oeriksson@mandriva.com> 1.6-1mdv2008.0
+ Revision: 62241
- 1.6
- added P1,P2,P3 from gentoo but adapted P3 a bit


* Sun Feb 18 2007 Giuseppe GhibÃ² <ghibo@mandriva.com> 1.5-5mdv2007.0
+ Revision: 122424
- bunzip2 patches.
- Import jbigkit

* Sat Dec 31 2005 Mandriva Linux Team <http://www.mandrivaexpert.com/> 1.5-4mdk
- Rebuild

* Sat Mar 19 2005 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.5-3mdk
- Backported patches from 1.6 to fix these bugs:
  - various small changes to reduce the risk of 32-bit unsigned
    integer overflows when dealing with extremely large images
  - robuster treatment of L0 = 0xffffffff.
  - minor API modification in jbg_enc_options(): parameter l0 changed
    from type long to unsigned long; previous value now remains
    unchanged when l0 == 0 (was: l0 < 0).

