# defining macros needed by SELinux
%global selinuxtype targeted
%global selinux_policyver 3.14.1
%global moduletype contrib
%global modulename tabrmd

Name: tpm2-abrmd-selinux
Version: 2.3.1
Release: 1%{?dist}
Summary: SELinux policies for tpm2-abrmd

License: BSD
URL:     https://github.com/tpm2-software/tpm2-abrmd
Source0: https://github.com/tpm2-software/tpm2-abrmd/archive/%{version}/tpm2-abrmd-%{version}.tar.gz
Patch0: selinux-allow-fwupd-to-communicate-with-tpm2-abrmd.patch

BuildArch: noarch
Requires: selinux-policy >= %{selinux_policyver}
Requires: selinux-policy-%{selinuxtype} >= %{selinux_policyver}
BuildRequires: git
BuildRequires: pkgconfig(systemd)
BuildRequires: selinux-policy
BuildRequires: selinux-policy-devel
Requires(pre): libselinux-utils
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
* Mon Nov 16 2020 Jerry Snitselaar <jsnitsel@redhat.com> - 2.3.3-1
- Rebase to 2.3.1 release
resolves: rhbz#1898384

* Tue May 14 2019 Jerry Snitselaar <jsnitsel@redhat.com> - 2.0.0-3
- Fix Requires issue.
- Add initial CI gating support.
resolves: rhbz#1642000, rhbz#1682415

* Tue Sep 11 2018 Jerry Snitselaar <jsnitsel@redhat.com> - 2.0.0-2
- Fix dependency
resolves: rhbz#1628771

* Wed Jul 04 2018 Javier Martinez Canillas <javierm@redhat.com> - 2.0.0-1
- Initial import (rhbz#1550595)
