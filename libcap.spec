#
# Conditional build:
%bcond_with	golang	# Go components (nothing useful yet?)

%ifnarch %{ix86} %{x8664} %{arm} aarch64 mips64 mips64le ppc64le
%undefine	with_golang
%endif
Summary:	POSIX.1e capability suite
Summary(pl.UTF-8):	Wsparcie dla standardu "capability" POSIX.1e
Summary(pt_BR.UTF-8):	Biblioteca para leitura e configuração de capabilities.
Name:		libcap
Version:	2.28
Release:	1
Epoch:		1
License:	GPL v2 or BSD
Group:		Applications/System
Source0:	https://www.kernel.org/pub/linux/libs/security/linux-privs/libcap2/%{name}-%{version}.tar.xz
# Source0-md5:	4066ddca53fb7e146f98372c8e43afc4
Patch0:		%{name}-make.patch
URL:		https://sites.google.com/site/fullycapable/
BuildRequires:	attr-devel
%{?with_golang:BuildRequires:	golang}
BuildRequires:	pam-devel
BuildRequires:	perl-base
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
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

%package libs
Summary:	libcap library
Summary(pl.UTF-8):	Biblioteka libcap
Group:		Libraries
Conflicts:	libcap < 1:2.16-2

%description libs
libcap library.

%description libs -l pl.UTF-8
Biblioteka libcap.

%package devel
Summary:	Header files and development documentation for libcap
Summary(pl.UTF-8):	Pliki nagłówkowe i dokumentacja do libcap
Summary(pt_BR.UTF-8):	Arquivos de desenvolvimento para capabilities
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description devel
Header files and development documentation for libcap.

%description devel -l pl.UTF-8
Pliki nagłówkowe i dokumentacja do libcap.

%description devel -l pt_BR.UTF-8
Arquivos de desenvolvimento para capabilities.

%package static
Summary:	Static libcap library
Summary(pl.UTF-8):	Statyczna biblioteka libcap
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static libcap library.

%description static -l pl.UTF-8
Statyczna biblioteka libcap.

%package -n pam-pam_cap
Summary:	Capability module for PAM
Summary(pl.UTF-8):	Moduł PAM capability
Group:		Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	pam

%description -n pam-pam_cap
PAM capability module enforces inheritable capability sets.

%description -n pam-pam_cap -l pl.UTF-8
Moduł PAM capability wymuszający dziedziczone zbiory uprawnień.

%prep
%setup -q
%patch0 -p1

%build
%{__make} -j1 \
	CC="%{__cc}" \
	DEBUG= \
	%{!?with_golang:GOLANG=0} \
	OPT_CFLAGS="-Iinclude %{rpmcflags} %{rpmcppflags}" \
	OPT_LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	FAKEROOT=$RPM_BUILD_ROOT \
	%{!?with_golang:GOLANG=0} \
	RAISE_SETFCAP=no \
	lib=%{_lib}

cp -p libcap/libpsx.a $RPM_BUILD_ROOT%{_libdir}

install -d $RPM_BUILD_ROOT/%{_lib}/security
install -p pam_cap/pam_cap.so $RPM_BUILD_ROOT/%{_lib}/security
install -d $RPM_BUILD_ROOT/etc/security
cp -a pam_cap/capability.conf $RPM_BUILD_ROOT/etc/security

install -d $RPM_BUILD_ROOT%{_libdir}
ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libcap.so.*.*) \
	$RPM_BUILD_ROOT%{_libdir}/libcap.so
%{__rm} $RPM_BUILD_ROOT/%{_lib}/libcap.so
%{__mv} $RPM_BUILD_ROOT/%{_lib}/libcap.a $RPM_BUILD_ROOT%{_libdir}

chmod a+x $RPM_BUILD_ROOT/%{_lib}/*.so*

%clean
rm -rf $RPM_BUILD_ROOT

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG License README
%attr(755,root,root) %{_sbindir}/capsh
%attr(755,root,root) %{_sbindir}/getcap
%attr(755,root,root) %{_sbindir}/getpcaps
# TODO: cap_setfcap=i
%attr(755,root,root) %{_sbindir}/setcap
%{_mandir}/man1/capsh.1*
%{_mandir}/man8/getcap.8*
%{_mandir}/man8/setcap.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libcap.so.*.*
%attr(755,root,root) %ghost /%{_lib}/libcap.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcap.so
%{_libdir}/libpsx.a
%{_includedir}/sys/capability.h
%{_pkgconfigdir}/libcap.pc
%{_mandir}/man3/libcap*.3*
%{_mandir}/man3/cap_*
%{_mandir}/man3/capgetp.3*
%{_mandir}/man3/capsetp.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libcap.a

%files -n pam-pam_cap
%defattr(644,root,root,755)
%doc pam_cap/License
%attr(755,root,root) /%{_lib}/security/pam_cap.so
%config(noreplace) %verify(not md5 mtime size) /etc/security/capability.conf
