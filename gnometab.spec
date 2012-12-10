%define name	gnometab
%define version	0.7.4
%define release	 %mkrel 8

Summary:	Gnometab aims to be a WYSIWYG guitar tablature editor
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Sound
URL:		http://www.solutionm.com/gnometab/
Source0:	%{name}-%{version}.tar.bz2
Source1:	%{name}_16.png
Source2:	%{name}_32.png
Source3:	%{name}_48.png
Patch0:		%{name}-0.7.4-schemas.patch.bz2
Patch1:		%{name}-0.7.4-depr.patch.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	libgnomeui2-devel
BuildRequires:	libgnomeprintui-devel
Requires(post,preun):		GConf2 >= 2.3.3

%description
Gnometab aims to be a WYSIWYG (what you see is what you get) tablature editor.
Gnometab's features include copying and pasting of tablature passages, a
chord library (which the user must fill with chords), professional-looking
rhythm notation (not perfect yet), the ability to create a variety of
tablature symbols specific to the guitar -- bends, slurs (hammer-ons,
pull-offs, etc.), etc.
And, of course, clean-looking printed output, given any postscript-compatible 
printer.  Gnometab does not attempt to be "smart", i.e., it does not know how 
many beats are in a measure, nor does it know an E chord from an Am chord.  
Instead, the emphasis has been on the appearance of the output.

%prep
%setup -q
%patch0 -p1 -b .schemas-fix
%patch1 -p1 -b .deprecated

%build
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT

export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
%makeinstall_std
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

rm -rf $RPM_BUILD_ROOT%{_prefix}/doc

# Menu
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application <<EOF
Exec=%{_bindir}/%{name}
Icon=AudioVideo;Player;Audio;
Categories=Multimedia/Sound
Name=Gnometab
Comment=Gnometab is a guitar tablature editor.
EOF

#icon
install -D -m 0644 %{SOURCE1} $RPM_BUILD_ROOT/%{_miconsdir}/%{name}.png
install -D -m 0644 %{SOURCE2} $RPM_BUILD_ROOT/%{_iconsdir}/%{name}.png
install -D -m 0644 %{SOURCE3} $RPM_BUILD_ROOT/%{_liconsdir}/%{name}.png

%if %mdkversion < 200900
%post
%{update_menus}
%post_install_gconf_schemas gnometab
%endif

%preun
%preun_uninstall_gconf_schemas gnometab

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%clean
rm -fr $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc ChangeLog README TODO
%{_bindir}/*
%{_datadir}/pixmaps/*
%{_datadir}/gnome/apps/Applications/gnometab.desktop
%{_sysconfdir}/gconf/schemas/gnometab.schemas
%{_datadir}/applications/mandriva-*.desktop
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png




%changelog
* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 0.7.4-8mdv2011.0
+ Revision: 619162
- the mass rebuild of 2010.0 packages

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 0.7.4-7mdv2010.0
+ Revision: 429262
- rebuild

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 0.7.4-6mdv2009.0
+ Revision: 246465
- rebuild
- fix description-line-too-long

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - use %%post_install_gconf_schemas/%%preun_uninstall_gconf_schemas

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Dec 17 2007 Thierry Vignaud <tv@mandriva.org> 0.7.4-4mdv2008.1
+ Revision: 131654
- auto-convert XDG menu entry
- fix prereq
- kill re-definition of %%buildroot on Pixel's request
- use %%mkrel
- fix summary-ended-with-dot
- import gnometab


* Fri Nov 04 2005 Marcel Pol <mpol@mandriva.org> 0.7.4-4mdk
- rebuild

* Thu Sep 02 2004 Marcel Pol <mpol@mandrake.org> 0.7.4-3mdk
- patch1 fix compile

* Mon Aug 11 2003 Abel Cheung <maddog@linux.org.hk> 0.7.4-2mdk
- Patch0: Fix schemas list type error
- misc spec fixes
- Uninstall schemas at preun

* Wed Apr 30 2003 Marcel Pol <mpol@gmx.net> 0.7.4-1mdk
- initial mandrake release
