Summary:	POSIX.1e capability suite
Summary(pl.UTF-8):	Wsparcie dla standardu "capability" POSIX.1e
Summary(pt_BR.UTF-8):	Biblioteca para leitura e configuração de capabilities.
Name:		libcap
Version:	2.06
Release:	1
Epoch:		1
License:	GPL or BSD
Group:		Applications/System
Source0:	ftp://ftp.kernel.org/pub/linux/libs/security/linux-privs/libcap2/%{name}-%{version}.tar.gz
# Source0-md5:	18f236fbd4a3613edb194f1792ad0a69
Patch0:		%{name}-make.patch
Patch1:		%{name}-pam-conf.patch
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
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	pam

%description -n pam-pam_cap
PAM capability module enforces inheritable capability sets.

%description -n pam-pam_cap -l pl.UTF-8
Moduł PAM capability wymuszający dziedziczone zbiory uprawnień.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__make} \
	CC="%{__cc}" \
	COPTFLAG="%{rpmcflags}" \
	DEBUG= \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	FAKEROOT=$RPM_BUILD_ROOT \
	lib=%{_lib}

install -d $RPM_BUILD_ROOT/%{_lib}/security
install pam_cap/pam_cap.so $RPM_BUILD_ROOT/%{_lib}/security
install -d $RPM_BUILD_ROOT/etc/security
install pam_cap/capability.conf $RPM_BUILD_ROOT/etc/security

install -d $RPM_BUILD_ROOT%{_libdir}
install libcap/libcap.a $RPM_BUILD_ROOT%{_libdir}
ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libcap.so.*.*) \
	$RPM_BUILD_ROOT%{_libdir}/libcap.so
rm $RPM_BUILD_ROOT/%{_lib}/libcap.so

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
%attr(755,root,root) %{_sbindir}/capsh
%attr(755,root,root) %{_sbindir}/getcap
%attr(755,root,root) %{_sbindir}/getpcaps
%attr(755,root,root) %{_sbindir}/setcap
%attr(755,root,root) /%{_lib}/libcap.so.*.*
%attr(755,root,root) %ghost /%{_lib}/libcap.so.2
%{_mandir}/man8/getcap.8*
%{_mandir}/man8/setcap.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcap.so
%{_includedir}/sys/capability.h
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
