%define lib_name %mklibname cddb-slave 2 %{lib_major}
%define develname %mklibname -d cddb-slave 2
%define lib_major 0
%define req_gail_version			0.13
%define req_gstreamer_version		0.10

Summary:	GNOME media programs
Name:		gnome-media
Version: 2.19.92
Release: %mkrel 2
License:	LGPL
Group:		Graphical desktop/GNOME
BuildRequires:	libgnomeui2-devel >= 2.13.2
BuildRequires:	ncurses-devel scrollkeeper sendmail-command
BuildRequires: gail-devel >= %{req_gail_version}
BuildRequires: libgstreamer-plugins-base-devel >= %{req_gstreamer_version}
BuildRequires: gstreamer0.10-plugins-base
BuildRequires:   gstreamer0.10-plugins-good
BuildRequires: libGConf2-devel
BuildRequires: libglade2.0-devel
BuildRequires: libnautilus-burn-devel >= 2.9.0
BuildRequires: libxrender-devel
BuildRequires: gnome-doc-utils
BuildRequires: perl-XML-Parser
BuildRequires: desktop-file-utils
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
Patch: gnome-media-2.19.92-desktopentry.patch
# (fc) 2.3.90-2mdk disable sound event if needed
Patch2:		gnome-media-2.14.0-esd.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
URL:		http://www.gnome.org/
Requires:   gstreamer0.10-cdparanoia >= %{req_gstreamer_version}
Requires:   gstreamer0.10-plugins-good
Requires:   gstreamer0.10-plugins-base
Requires:   gstreamer0.10-flac
Requires:   gstreamer0.10-speex
Obsoletes:	grecord
Provides:	grecord
Requires(post):	scrollkeeper >= 0.3
Requires(postun):	scrollkeeper >= 0.3
Requires(post):	GConf2 >= 2.3.3
Requires(preun):	GConf2 >= 2.3.3

%description
GNOME (GNU Network Object Model Environment) is a user-friendly set
of applications and desktop tools to be used in conjunction with
a window manager for the X Window System. GNOME is similar
in purpose and scope to CDE and KDE, but GNOME (as KDE) 
is based completely on Open Source software.

GNOME's powerful environment is pleasing on the eye, easy to
configure and use.

This package will install such media features as the GNOME
CD player.

%package -n %{lib_name}
Summary:	%{summary}
Group:		%{group}
Requires:	%{name} >= %{version}

%description -n %{lib_name}
libraries for running GNOME media.

%package -n %develname
Summary:	Static libraries, include files for GNOME media
Group:		Development/GNOME and GTK+
Provides:	libcddb-slave2-devel = %{version}-%{release}
Requires:	%{lib_name} = %{version}-%{release}
Obsoletes: %mklibname -d cddb-slave 2 0

%description -n %develname
Panel libraries and header files for GNOME media.



%prep
%setup -q 
%patch -p1
%patch2 -p1 -b .esd

%build

%configure2_5x

%make

%install
rm -rf $RPM_BUILD_ROOT

GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std

rm -f %buildroot%{_libdir}/libglade/2.0/libgnome-media-profiles.a

desktop-file-install --vendor="" \
  --add-category="DesktopSettings" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/{gstreamer-properties.desktop,cddb-slave.desktop}

# don't display vumeter / reclevel in menu
echo 'NoDisplay=true' >>$RPM_BUILD_ROOT%{_datadir}/applications/vumeter.desktop
echo 'NoDisplay=true' >>$RPM_BUILD_ROOT%{_datadir}/applications/reclevel.desktop

#hide gnome-volume-control in KDE
echo 'NotShowIn=KDE;' >>$RPM_BUILD_ROOT%{_datadir}/applications/gnome-volume-control.desktop


%find_lang %{name}-2.0 --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_scrollkeeper
%define schemas CDDB-Slave2 gnome-cd gnome-sound-recorder gnome-audio-profiles gnome-volume-control
%post_install_gconf_schemas %schemas
%{update_menus}
%update_icon_cache hicolor

%preun
%preun_uninstall_gconf_schemas %schemas

%postun
%clean_scrollkeeper
%{clean_menus}
%clean_icon_cache hicolor

%post -p /sbin/ldconfig -n %{lib_name}

%postun -p /sbin/ldconfig -n %{lib_name}

%files -f  %{name}-2.0.lang
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_sysconfdir}/gconf/schemas/CDDB-Slave2.schemas
%{_sysconfdir}/gconf/schemas/gnome-cd.schemas
%{_sysconfdir}/gconf/schemas/gnome-sound-recorder.schemas
%{_sysconfdir}/gconf/schemas/gnome-audio-profiles.schemas
%{_sysconfdir}/gconf/schemas/gnome-volume-control.schemas
%{_bindir}/*
%{_libexecdir}/CDDBSlave2
%{_libexecdir}/cddb-track-editor
%{_libdir}/bonobo/servers/*
%{_libdir}/libglade/2.0/libgnome-media-profiles.so
%{_libdir}/libglade/2.0/libgnome-media-profiles.la
%{_datadir}/applications/cddb-slave.desktop
%{_datadir}/applications/gnome-cd.desktop
%{_datadir}/applications/gnome-sound-recorder.desktop
%{_datadir}/applications/gnome-volume-control.desktop
%{_datadir}/applications/gstreamer-properties.desktop
%{_datadir}/applications/reclevel.desktop
%{_datadir}/applications/vumeter.desktop
%{_datadir}/gnome-media
%{_datadir}/gnome-sound-recorder
%{_datadir}/gstreamer-properties
%{_datadir}/pixmaps/*
%_datadir/icons/hicolor/*/*/*.*
%{_datadir}/idl/*

%files -n  %{lib_name}
%defattr(-, root, root)
%{_libdir}/libcddb-slave2.so.%{lib_major}*
%{_libdir}/libgnome-media-profiles.so.%{lib_major}*

%files -n  %develname
%defattr(-, root, root)
%{_libdir}/*.so
%attr(644,root,root) %{_libdir}/*.la
%{_libdir}/*.a
%{_libdir}/pkgconfig/gnome-media-profiles.pc
%{_includedir}/*


