Summary:	POSIX.1e capability suite
Summary(pl):	Wsparcie dla standardu POSIX.1e
Name:		libcap
Version:	0.122
Release:	2
Copyright:	BSD or GNU GPL
Group:		Utilities/System
Source:		ftp://ftp.kernel.org/pub/linux/libs/security/linux-privs/kernel-2.1/%{name}-%{version}.tar.bz2
Icon:		libcap.gif
URL:		http://linux.kernel.org/pub/linux/libs/security/linux-privs/
Buildroot:	/tmp/%{name}-%{version}-root
Conflicts:	glibc <= 2.0.7

%description
The POSIX.1e capability library for Linux. This package contains the
getcap and setcap binaries and manual pages.

%description -l pl
Biblioteka, programy oraz strony manuala zawieraj±ce implementacje 
standardu POSIX.1e. 

%package devel
Summary:	Header files and development dovumentation for libcap
Summary(pl):	Pliki nag³ówkowe i dokumentacja do libcap
Group:		Development/Libraries
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel
Header files and development dovumentation for libcap.

%description -l pl devel
Pliki nag³ówkowe i dokumentacja do libcap.

%prep
%setup -q

%build
make "COPTFLAGS=$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
make install FAKEROOT=$RPM_BUILD_ROOT

gzip -9nf $RPM_BUILD_ROOT/usr/man/man*/*

strip $RPM_BUILD_ROOT/lib/lib*so.*.*

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%attr(755,root,root) /lib/lib*.so.*.*
%attr(755,root,root) /sbin/*
%attr(644,root,root) /usr/man/man2/*

%files devel
%defattr(644,root,root,755)
%doc README 
%attr(755,root,root) /lib/lib*.so.*.*
/usr/man/man3/*
/usr/include/sys/capability.h

%changelog
* Thu Mar 11 1999 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [0.122-2]
- added URL,
- added devel subpackage,
- added stripping shared libraries,
- added "Conflicts: glibc <= 2.0.7" for installing libcap in proper
  enviroment,
- removed man group from man pages.

* Tue Sep 22 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [0.122-1d]
- updated to 0.122, 
- added %changelog,
- translation modified for pl
  (translation prepared by Krzysztof Baranowski <kgb@knm.org.pl>).
