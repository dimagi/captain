(function() {
    "strict"

    window.Chief = {
        ViewModels: {}
    };

    Chief.ViewModels.InitiateDeploy = function() {
        var self = this;
        self.env = ko.observable(null);

        $('#deploy-modal').on('show.bs.modal', function(e) {
            var $btn = $(e.relatedTarget);
            console.log($btn.data('environment'))
            self.env($btn.data('environment'));
        });

        self.env.subscribe(function(newEnv) {
            var data = {
                env: newEnv,
                csrfmiddlewaretoken: Chief.config.csrfmiddlewaretoken
            };
            $.post(Chief.config.prepareUrl, data).done(function(response) {
                console.log(response);
                return $.get(Chief.config.submodulesUrl, { env: newEnv }).done(function(response) {
                    console.log(response);
                    self.submodules(response.submodules);
                });
            })
        });
        self.submodules = ko.observableArray([]);
        self.submoduleToCommit = ko.observableArray([]);
        self.initiateDeploy = function() {
            $('#deploy-form').submit();
        };
    };

    Chief.ViewModels.PreviousReleases = function() {
        var self = this;
        self.init();
        self.environments = ko.observableArray([]);
        self.releases = ko.observableArray([]);

    };
    Chief.ViewModels.PreviousReleases.prototype.init = function() {
        var self = this;
        //$.get(Chief.config.releasesUrl).done(function(response) {
        //    console.log(response);
        //    self.environments(_.keys(response));
        //    _.each(response, function(releases, env) {
        //        response[env] = _.map(releases, self.parseRelease);
        //    });
        //    self.releases(response);
        //});
    };
    Chief.ViewModels.PreviousReleases.prototype.parseRelease = function(release) {
        var dateParts = _.last(release.split('/')).split('_');
        // Convert the raw date format we use to ISO string
        var date = new Date(dateParts[0] + 'T' + dateParts[1].replace('.', ':') + ':00');
        console.log(date);
        return {
            path: release,
            date: date
        }

    };
})();
