Summary:	POSIX.1e capability suite
Summary(pl):	Wsparcie dla standardu POSIX.1e
Name:		libcap
Version:	1.03
Release:	1
Copyright:	BSD or GNU GPL
Group:		Utilities/System
Group(pl):	Narz璠zia/System
Source:		ftp://ftp.kernel.org/pub/linux/libs/security/linux-privs/kernel-2.2/%{name}-%{version}.tar.bz2
Icon:		libcap.gif
URL:		http://linux.kernel.org/pub/linux/libs/security/linux-privs/
Buildroot:	/tmp/%{name}-%{version}-root

%description
The POSIX.1e capability library for Linux. This package contains the
getcap and setcap binaries and manual pages.

%description -l pl
Biblioteka, programy oraz strony manuala zawieraj帷e implementacje 
standardu POSIX.1e. 

%package devel
Summary:	Header files and development dovumentation for libcap
Summary(pl):	Pliki nag堯wkowe i dokumentacja do libcap
Group:		Development/Libraries
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel
Header files and development dovumentation for libcap.

%description -l pl devel
Pliki nag堯wkowe i dokumentacja do libcap.

%prep
%setup -q

%build
make "COPTFLAGS=$RPM_OPT_FLAGS -g"

%install
rm -rf $RPM_BUILD_ROOT

make install \
	FAKEROOT=$RPM_BUILD_ROOT \
	MANDIR=$RPM_BUILD_ROOT%{_mandir}

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* README 

strip --strip-unneeded $RPM_BUILD_ROOT/lib/lib*so.*.*

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(755,root,root,755)

/lib/lib*.so.*.*
/sbin/*

%attr(644,root,root) %{_mandir}/man2/*

%files devel
%defattr(644,root,root,755)
%doc README.gz

%attr(755,root,root) /lib/lib*.so

%{_mandir}/man3/*
%{_includedir}/sys/capability.h

%changelog
* Sat May 29 1999 Tomasz K這czko <kloczek@rudy.mif.pg.gda.pl>
  [1.03-1]
- now package is FHS 2.0 compliant,
- recompiled on new rpm.

- more rpm macros.

* Sat Apr 24 1999 Tomasz K這czko <kloczek@rudy.mif.pg.gda.pl>
  [1.02-1]
- removed "Conflicts: glibc <= 2.0.7" (not neccessary now),
- recompiles on new rpm.

* Mon Mar 15 1999 Tomasz K這czko <kloczek@rudy.mif.pg.gda.pl>
  [1.0-1]
- strip shared libraries with --strip-unneeded.

* Sun Mar 14 1999 Wojtek 奸usarczyk <wojtek@shadow.eu.org>
- updated to 1.0,
- fixed duplicate libs in devel subpackage,
- added Group(pl) in main package,
- compressed documentation.

* Thu Mar 11 1999 Tomasz K這czko <kloczek@rudy.mif.pg.gda.pl>
  [0.122-2]
- added URL,
- added devel subpackage,
- added stripping shared libraries,
- added "Conflicts: glibc <= 2.0.7" for installing libcap in proper
  enviroment,
- removed man group from man pages.

* Tue Sep 22 1998 Wojtek 奸usarczyk <wojtek@shadow.eu.org>
  [0.122-1d]
- updated to 0.122, 
- added %changelog,
- translation modified for pl
  (prepared by Krzysztof Baranowski <kgb@knm.org.pl>),
- build against GNU libc-2.1.
