from django.contrib import admin


class SmarterModelAdmin(admin.ModelAdmin):
    valid_lookups = ()

    def lookup_allowed(self, lookup, *args, **kwargs):
        if lookup.startswith(self.valid_lookups):
            return True

        return super(SmarterModelAdmin, self).lookup_allowed(lookup, *args, **kwargs)
