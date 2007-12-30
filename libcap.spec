Summary:	POSIX.1e capability suite
Summary(pl.UTF-8):	Wsparcie dla standardu "capability" POSIX.1e
Summary(pt_BR.UTF-8):	Biblioteca para leitura e configuração de capabilities.
Name:		libcap
Version:	1.10
Release:	6
Epoch:		1
License:	GPL or BSD
Group:		Applications/System
Source0:	ftp://ftp.kernel.org/pub/linux/libs/security/linux-privs/kernel-2.2/%{name}-%{version}.tar.gz
# Source0-md5:	2c09eea823f67cfdde96177a959bc39b
Patch0:		%{name}-1.92-make.patch
Patch1:		%{name}-link.patch
URL:		http://www.kernel.org/pub/linux/libs/security/linux-privs/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir		/sbin

%description
The POSIX.1e capability library for Linux. This package contains the
getcap and setcap binaries and manual pages.

%description -l pl.UTF-8
Biblioteka, programy oraz strony manuala zawierające implementację
"capability" standardu POSIX.1e.

%description -l pt_BR.UTF-8
Biblioteca para leitura e configuração de capabilities.

%package devel
Summary:	Header files and development documentation for libcap
Summary(pl.UTF-8):	Pliki nagłówkowe i dokumentacja do libcap
Summary(pt_BR.UTF-8):	Arquivos de desenvolvimento para capabilities
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Header files and development documentation for libcap.

%description devel -l pl.UTF-8
Pliki nagłówkowe i dokumentacja do libcap.

%description devel -l pt_BR.UTF-8
Arquivos de desenvolvimento para capabilities.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__make} \
	CC="%{__cc}" \
	COPTFLAG="%{rpmcflags}" \
	LDFLAGS="%{rpmcflags} %{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	FAKEROOT=$RPM_BUILD_ROOT \
	LIBDIR=$RPM_BUILD_ROOT/%{_lib} \
	MANDIR=$RPM_BUILD_ROOT%{_mandir}

install -d $RPM_BUILD_ROOT%{_libdir}
ln -sf /%{_lib}/$(cd $RPM_BUILD_ROOT/%{_lib}; echo libcap.so.*.*) \
	$RPM_BUILD_ROOT%{_libdir}/libcap.so

# newer versions exist in man-pages
# and these syscalls are specific to Linux/glibc, not libcap
rm -f $RPM_BUILD_ROOT%{_mandir}/man2/cap{get,set}.2

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
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/sys/capability.h
%{_mandir}/man3/*
