Summary:	POSIX.1e capability suite
Summary(pl):	Wsparcie dla standardu "capability" POSIX.1e
Name:		libcap
Version:	1.92
Release:	1
License:	BSD or GNU GPL
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System
Source0:	ftp://ftp.kernel.org/pub/linux/libs/security/linux-privs/kernel-2.2/%{name}-%{version}.tar.gz
Patch0:		%{name}-1.92-make.patch
Icon:		libcap.gif
URL:		http://linux.kernel.org/pub/linux/libs/security/linux-privs/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The POSIX.1e capability library for Linux. This package contains the
getcap and setcap binaries and manual pages.

%description -l pl
Biblioteka, programy oraz strony manuala zawieraj±ce implementacjÍ
"capability" standardu POSIX.1e.

%package devel
Summary:	Header files and development documentation for libcap
Summary(pl):	Pliki nag≥Ûwkowe i dokumentacja do libcap
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	Ú¡⁄“¡¬œ‘À¡/‚…¬Ã…œ‘≈À…
Group(uk):	Úœ⁄“œ¬À¡/‚¶¬Ã¶œ‘≈À…
Requires:	%{name} = %{version}

%description devel
Header files and development documentation for libcap.

%description -l pl devel
Pliki nag≥Ûwkowe i dokumentacja do libcap.

%prep
%setup -q
%patch -p1

%build
%{__make} "COPTFLAGS=%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	FAKEROOT=$RPM_BUILD_ROOT \
	MANDIR=$RPM_BUILD_ROOT%{_mandir}

gzip -9nf README 

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) /lib/lib*.so.*.*
%attr(755,root,root) /sbin/*
%{_mandir}/man8/*

%files devel
%defattr(644,root,root,755)
%doc README.gz
%attr(755,root,root) /lib/lib*.so
%{_mandir}/man[23]/*
%{_includedir}/sys/capability.h
