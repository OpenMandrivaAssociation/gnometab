%define name	gnometab
%define version	0.7.4
%define release	 %mkrel 4

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

%post
%{update_menus}
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` \
%{_bindir}/gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/gnometab.schemas > /dev/null

%preun
if [ $1 -eq 0 ]; then
  GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` \
  %{_bindir}/gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/gnometab.schemas > /dev/null
fi

%postun
%{clean_menus}

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


