Summary:	POSIX.1e capability suite
Summary(pl):	Wsparcie dla standardu "capability" POSIX.1e
Summary(pt_BR):	Biblioteca para leitura e configuração de capabilities.
Name:		libcap
Version:	1.10
Release:	2
Epoch:		1
License:	GPL or BSD
Group:		Applications/System
Source0:	ftp://ftp.kernel.org/pub/linux/libs/security/linux-privs/kernel-2.2/%{name}-%{version}.tar.gz
# Source0-md5:	2c09eea823f67cfdde96177a959bc39b
Patch0:		%{name}-1.92-make.patch
Patch1:		%{name}-link.patch
Icon:		libcap.gif
URL:		http://www.kernel.org/pub/linux/libs/security/linux-privs/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir		/sbin

%description
The POSIX.1e capability library for Linux. This package contains the
getcap and setcap binaries and manual pages.

%description -l pl
Biblioteka, programy oraz strony manuala zawieraj±ce implementacjê
"capability" standardu POSIX.1e.

%description -l pt_BR
Biblioteca para leitura e configuração de capabilities.

%package devel
Summary:	Header files and development documentation for libcap
Summary(pl):	Pliki nag³ówkowe i dokumentacja do libcap
Summary(pt_BR):	Arquivos de desenvolvimento para capabilities
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}

%description devel
Header files and development documentation for libcap.

%description devel -l pl
Pliki nag³ówkowe i dokumentacja do libcap.

%description devel -l pt_BR
Arquivos de desenvolvimento para capabilities.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__make} \
	CC="%{__cc}" \
	COPTFLAG="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	FAKEROOT=$RPM_BUILD_ROOT \
	LIBDIR=$RPM_BUILD_ROOT/%{_lib} \
	MANDIR=$RPM_BUILD_ROOT%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG License README
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) /%{_lib}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/lib*.so
%{_mandir}/man[23]/*
%{_includedir}/sys/capability.h
