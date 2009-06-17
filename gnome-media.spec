%define lib_name %mklibname cddb-slave 2 %{lib_major}
%define develname %mklibname -d cddb-slave 2
%define lib_major 0
%define req_gail_version			0.13
%define req_gstreamer_version		0.10

Summary:	GNOME media programs
Name:		gnome-media
Version: 2.27.3
Release: %mkrel 1
License:	GPLv2+ and GFDL+
Group:		Graphical desktop/GNOME
BuildRequires:	libgnomeui2-devel >= 2.13.2
BuildRequires:	ncurses-devel scrollkeeper sendmail-command
BuildRequires: gail-devel >= %{req_gail_version}
BuildRequires: libgstreamer-plugins-base-devel >= %{req_gstreamer_version}
BuildRequires: gstreamer0.10-plugins-base
BuildRequires:   gstreamer0.10-plugins-good
BuildRequires: libGConf2-devel
BuildRequires: libglade2.0-devel
BuildRequires: libxrender-devel
BuildRequires: libcanberra-devel
BuildRequires: pulseaudio-devel
BuildRequires: unique-devel
BuildRequires: gnome-doc-utils
BuildRequires: intltool >= 0.35
BuildRequires: desktop-file-utils
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
URL:		http://www.gnome.org/
Requires:   gstreamer0.10-plugins-good
Requires:   gstreamer0.10-plugins-base
Suggests:   gstreamer0.10-flac
Suggests:   gstreamer0.10-speex
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

%package -n %{lib_name}
Summary:	%{summary}
Group:		System/Libraries
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

%build

%configure2_5x --disable-gnomecd 

%make

%install
rm -rf $RPM_BUILD_ROOT

GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std

rm -f %buildroot%{_libdir}/libglade/2.0/libgnome-media-profiles.a

desktop-file-install --vendor="" \
  --add-category="DesktopSettings" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/gstreamer-properties.desktop

desktop-file-install --vendor="" \
  --add-category="X-MandrivaLinux-CrossDesktop" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/gnome-sound-recorder.desktop


%find_lang %{name}-2.0 --with-gnome --all-name
for omf in %buildroot%_datadir/omf/*/{*-??.omf,};do
echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed s!%buildroot!!)" >> %name-2.0.lang
done

%clean
rm -rf $RPM_BUILD_ROOT

%post
%define schemas gnome-sound-recorder gnome-audio-profiles
%if %mdkversion < 200900
%update_scrollkeeper
%endif
%if %mdkversion < 200900
%post_install_gconf_schemas %schemas
%{update_menus}
%update_icon_cache hicolor
%endif

%preun
%preun_uninstall_gconf_schemas %schemas

%if %mdkversion < 200900
%postun
%clean_scrollkeeper
%{clean_menus}
%clean_icon_cache hicolor
%endif

%if %mdkversion < 200900
%post -p /sbin/ldconfig -n %{lib_name}
%endif

%if %mdkversion < 200900
%postun -p /sbin/ldconfig -n %{lib_name}
%endif

%files -f  %{name}-2.0.lang
%defattr(-, root, root)
%doc AUTHORS NEWS README
%_sysconfdir/xdg/autostart/gnome-volume-control-applet.desktop
%{_sysconfdir}/gconf/schemas/gnome-sound-recorder.schemas
%{_sysconfdir}/gconf/schemas/gnome-audio-profiles.schemas
%{_bindir}/*
%{_libdir}/libglade/2.0/libgnome-media-profiles.so
%{_libdir}/libglade/2.0/libgnome-media-profiles.la
%{_datadir}/applications/gnome-sound-recorder.desktop
%{_datadir}/applications/gnome-volume-control.desktop
%{_datadir}/applications/gstreamer-properties.desktop
%{_datadir}/gnome-media
%{_datadir}/gnome-sound-recorder
%{_datadir}/gstreamer-properties
%_datadir/icons/hicolor/*/*/*.*
%dir %_datadir/sounds/
%dir %_datadir/sounds/gnome/
%_datadir/sounds/gnome/default/

%files -n  %{lib_name}
%defattr(-, root, root)
%{_libdir}/libgnome-media-profiles.so.%{lib_major}*

%files -n  %develname
%defattr(-, root, root)
%{_libdir}/*.so
%attr(644,root,root) %{_libdir}/*.la
%{_libdir}/*.a
%{_libdir}/pkgconfig/gnome-media-profiles.pc
%{_includedir}/*
