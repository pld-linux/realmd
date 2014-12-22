# TODO: verify heimdal patch, complete pld patch
#
# Conditional build:
%bcond_with	krb5	# use MIT KRB5 instead of Heimdal Kerberos
#
Summary:	D-Bus service for configuring Kerberos and other online identities
Summary(pl.UTF-8):	Usługa D-Bus do konfigurowania Kerberosa i innych tożsamości w sieci
Name:		realmd
Version:	0.14.5
Release:	1
License:	LGPL v2+
Group:		Applications/System
Source0:	http://www.freedesktop.org/software/realmd/releases/%{name}-%{version}.tar.gz
# Source0-md5:	18ed8480e0fd9a1badb8f4504dafd5e0
Patch0:		%{name}-pld.patch
Patch1:		%{name}-heimdal.patch
URL:		http://www.freedesktop.org/software/realmd/
BuildRequires:	PackageKit-devel
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	docbook-style-xsl
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.32.0
%{!?with_krb5:BuildRequires:	heimdal-devel}
BuildRequires:	intltool >= 0.35.0
%{?with_krb5:BuildRequires:	krb5-devel}
BuildRequires:	libxslt-progs
BuildRequires:	openldap-devel
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel
BuildRequires:	systemd-devel
BuildRequires:	xmlto
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
D-Bus service for configuring Kerberos and other online identities.

%description -l pl.UTF-8
Usługa D-Bus do konfigurowania Kerberosa i innych tożsamości w sieci.

%prep
%setup -q
%patch0 -p1
%{!?with_krb5:%patch1 -p1}

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
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
%doc AUTHORS ChangeLog NEWS README doc/internals/html/*
%attr(755,root,root) %{_sbindir}/realm
%dir %{_libdir}/realmd
%attr(755,root,root) %{_libdir}/realmd/realmd
%{_libdir}/realmd/realmd-defaults.conf
%{_libdir}/realmd/realmd-distro.conf
/etc/dbus-1/system.d/org.freedesktop.realmd.conf
%{systemdunitdir}/realmd.service
%{_datadir}/dbus-1/system-services/org.freedesktop.realmd.service
%{_datadir}/polkit-1/actions/org.freedesktop.realmd.policy
%dir /var/cache/realmd
%dir /var/lib/realmd
%{_mandir}/man5/realmd.conf.5*
%{_mandir}/man8/realm.8*
%{_docdir}/realmd
