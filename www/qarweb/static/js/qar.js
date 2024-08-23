$(async () => {
    async function setPage(page, back = false) {
        var hash = `#${page}`;
        var label = getLabelForHash(hash);
        console.log("wizard label", label);

        if (label) {
            setWizardDropdownTitle(label);
        }

        if (window.location.hash !== hash) {
            window.location.hash = hash;
        }

        const current = $('.page.visible');

        if (current.length) {
            if (back) {
                current.addClass('trans-out-cancel');
            } else {
                current.addClass('trans-out-accept')
            }
            
            current.addClass('trans-out').removeClass('active');
            await new Promise(resolve => setTimeout(resolve, 666));
            current.removeClass('visible').removeClass('trans-out').removeClass('trans-out-cancel').removeClass('trans-out-accept');
        }

        const next = $(`#page-${page}`);

        next.addClass('visible').addClass('trans-in');
        await new Promise(resolve => setTimeout(resolve, 666));
        next.removeClass('trans-in').addClass('active');
        
        $(document).trigger('page-changed', page);
    }

    $('[data-page]').click(async function() {
        const page = $(this).data('page');
        const back = Boolean($(this).data('page-back'));
        setPage(page, back);
    });

    function getLabelForHash(hash) {
        if (hash.startsWith('#')) {
            hash = hash.replace('#', '');
        }

        const label = $(`#wizard-steps-dropdown a[href="#${hash}"]`);

        if (!label) {
            return '';
        }

        return $(label[0]).text().trim();
    }

    function setWizardDropdownTitle(title) {
        $('#wizard-steps-dropdown > .dropdown-toggle').text(title);
    }

    $(window).on('hashchange', function () {
        var hash = window.location.hash;

        if (hash === '') {
            hash = '#welcome';
        }

        setPage(hash.replace('#', ''));
    });

    if (window.location.hash === '') {
        window.location.hash = '#wizard-welcome';
    } else {
        setPage(window.location.hash.replace('#', ''));
    }

    //setPage('wizard-welcome');
});