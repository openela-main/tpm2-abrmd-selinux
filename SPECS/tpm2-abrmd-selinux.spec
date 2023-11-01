# defining macros needed by SELinux
%global selinuxtype targeted
%global selinux_policyver 3.14.3-22
%global moduletype contrib
%global modulename tabrmd

Name: tpm2-abrmd-selinux
Version: 2.3.1
Release: 7%{?dist}
Summary: SELinux policies for tpm2-abrmd

License: BSD
URL:     https://github.com/tpm2-software/tpm2-abrmd
Source0: https://github.com/tpm2-software/tpm2-abrmd/archive/%{version}/tpm2-abrmd-%{version}.tar.gz

Patch0: selinux-allow-fwupd-to-communicate-with-tpm2-abrmd.patch
Patch1: 0001-Add-new-interfaces-for-communication-with-keylime.patch
Patch2: 0002-Fix-in-SELinux-interface-file-a-typo.patch

BuildArch: noarch
Requires: selinux-policy >= %{selinux_policyver}
BuildRequires: make
BuildRequires: git
BuildRequires: pkgconfig(systemd)
BuildRequires: selinux-policy
BuildRequires: selinux-policy-devel
BuildRequires: selinux-policy-%{selinuxtype}
Requires(post): selinux-policy-base >= %{selinux_policyver}
Requires(post): libselinux-utils
Requires(post): policycoreutils
Requires(post): policycoreutils-python-utils

%description
SELinux policy modules for tpm2-abrmd.

%prep
%autosetup -p1 -n tpm2-abrmd-%{version}

%build
pushd selinux
make %{?_smp_mflags} TARGET="tabrmd" SHARE="%{_datadir}"
popd

%pre
%selinux_relabel_pre -s %{selinuxtype}

%install
# install policy modules
pushd selinux
install -d %{buildroot}%{_datadir}/selinux/packages
install -d -p %{buildroot}%{_datadir}/selinux/devel/include/%{moduletype}
install -p -m 644 %{modulename}.if %{buildroot}%{_datadir}/selinux/devel/include/%{moduletype}
install -m 0644 %{modulename}.pp.bz2 %{buildroot}%{_datadir}/selinux/packages
popd

%check

%post
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{modulename}.pp.bz2

%postun
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} %{modulename}
fi

%posttrans
%selinux_relabel_post -s %{selinuxtype}

%files
%license LICENSE
%{_datadir}/selinux/*
%{_datadir}/selinux/packages/%{modulename}.pp.bz2
%{_datadir}/selinux/devel/include/%{moduletype}/%{modulename}.if

%changelog
* Fri Jan 6 2023 Štěpán Horáček <shoracek@redhat.com> - 2.3.1-7
- Include interface for Keylime
  Resolves: rhbz#2157894

* Tue Aug 10 2021 Mohan Boddu <mboddu@redhat.com> - 2.3.1-6
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 2.3.1-5
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Wed Feb 17 2021 Jerry Snitselaar <jsnitsel@redhat.com> - 2.3.1-4
- Fix dependency.
Resolves: rhbz#1929701

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Feb 12 2020 Javier Martinez Canillas <javierm@redhat.com> - 2.3.1-1
- Update to 2.3.1 release

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Mar 08 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.1.0-2
- selinux: allow tpm2-abrmd to communicate with fwupd
  Resolves: rhbz#1665701

* Fri Feb 22 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.1.0-1
- Update to 2.1.0 release
- Add selinux-policy-%{selinuxtype} BuildRequires

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 04 2018 Javier Martinez Canillas <javierm@redhat.com> - 2.0.0-1
- Initial import (rhbz#1550595)
