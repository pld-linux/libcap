Summary:	POSIX.1e capability suite
Summary(pl):	Wsparcie dla standardu "capability" POSIX.1e
Name:		libcap
Version:	1.92
Release:	3
License:	GPL/BSD
Group:		Applications/System
Source0:	ftp://ftp.kernel.org/pub/linux/libs/security/linux-privs/kernel-2.2/%{name}-%{version}.tar.gz
Patch0:		%{name}-1.92-make.patch
Icon:		libcap.gif
URL:		http://linux.kernel.org/pub/linux/libs/security/linux-privs/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir		/sbin

%description
The POSIX.1e capability library for Linux. This package contains the
getcap and setcap binaries and manual pages.

%description -l pl
Biblioteka, programy oraz strony manuala zawierające implementację
"capability" standardu POSIX.1e.

%package devel
Summary:	Header files and development documentation for libcap
Summary(pl):	Pliki nagłówkowe i dokumentacja do libcap
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Header files and development documentation for libcap.

%description -l pl devel
Pliki nagłówkowe i dokumentacja do libcap.

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

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) /lib/lib*.so.*.*
%{_mandir}/man8/*

%files devel
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) /lib/lib*.so
%{_mandir}/man[23]/*
%{_includedir}/sys/capability.h
