# TODO: verify heimdal patch, complete pld patch
#
# Conditional build:
%bcond_with	krb5	# use MIT KRB5 instead of Heimdal Kerberos
#
Summary:	D-Bus service for configuring Kerberos and other online identities
Summary(pl.UTF-8):	Usługa D-Bus do konfigurowania Kerberosa i innych tożsamości w sieci
Name:		realmd
Version:	0.17.1
Release:	1
License:	LGPL v2+
Group:		Applications/System
#Source0Download: https://gitlab.freedesktop.org/realmd/realmd/-/releases
Source0:	https://gitlab.freedesktop.org/realmd/realmd/uploads/204d05bd487908ece2ce2705a01d2b26/%{name}-%{version}.tar.gz
# Source0-md5:	1027e0e0b6b1a92b5aa8a8342acab3ed
Patch0:		%{name}-pld.patch
Patch1:		%{name}-heimdal.patch
URL:		https://www.freedesktop.org/software/realmd/
BuildRequires:	PackageKit-devel
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	docbook-style-xsl
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.36.0
%{!?with_krb5:BuildRequires:	heimdal-devel}
BuildRequires:	intltool >= 0.35.0
%{?with_krb5:BuildRequires:	krb5-devel}
BuildRequires:	libxslt-progs
BuildRequires:	openldap-devel
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel
BuildRequires:	systemd-devel
BuildRequires:	xmlto
Requires:	glib2 >= 1:2.36.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if "%{_libexecdir}" == "%{_libdir}"
%define		pkglibexecdir	%{_prefix}/lib/realmd
%else
%define		pkglibexecdir	%{_libexecdir}
%endif

%description
D-Bus service for configuring Kerberos and other online identities.

%description -l pl.UTF-8
Usługa D-Bus do konfigurowania Kerberosa i innych tożsamości w sieci.

%prep
%setup -q
%patch -P0 -p1
%{!?with_krb5:%patch -P1 -p1}

%build
%{__aclocal} -I build/m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--libexecdir=%{pkglibexecdir} \
	--disable-silent-rules \
	--with-distro=pld \
	--with-systemd-unit-dir=%{systemdunitdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README internals/*
%attr(755,root,root) %{_sbindir}/realm
%dir %{_prefix}/lib/realmd
%{pkglibexecdir}/realmd
%{_prefix}/lib/realmd/realmd-defaults.conf
%{_prefix}/lib/realmd/realmd-distro.conf
/etc/dbus-1/system.d/org.freedesktop.realmd.conf
%{systemdunitdir}/realmd.service
%{_datadir}/dbus-1/system-services/org.freedesktop.realmd.service
%{_datadir}/polkit-1/actions/org.freedesktop.realmd.policy
%dir /var/cache/realmd
%dir /var/lib/realmd
%{_mandir}/man5/realmd.conf.5*
%{_mandir}/man8/realm.8*
%{_docdir}/realmd
