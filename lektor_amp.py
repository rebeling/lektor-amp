# -*- coding: utf-8 -*-

import types
from distutils.util import strtobool

from lektor.builder import Artifact
from lektor.context import get_ctx
from lektor.pluginsystem import Plugin
from lektor.reporter import reporter


def render_template_into(self, template_name, this, **extra):
    """Render a template into the artifact and an amp subartifact."""
    values = extra.get('values', {})
    values['canonical'] = self.artifact_name
    values['amp_path'] = ''
    extra['values'] = values

    if self.dst_filename.endswith('.html'):
        amp_path = '/amp/{}'.format(self.artifact_name)
        values['amp_path'] = amp_path
        rv2 = self.build_state.env.render_template(
            'amp-{}'.format(template_name), self.build_state.pad,
            this=this, **extra)

        ctx = get_ctx()

        @ctx.sub_artifact(amp_path)
        def build_ampsite(artifact):
            artifact.sources = self.sources
            with artifact.open('w') as f:
                f.write(rv2.encode('utf-8') + b'\n')

    rv = self.build_state.env.render_template(
        template_name, self.build_state.pad,
        this=this, **extra)
    with self.open('wb') as f:
        f.write(rv.encode('utf-8') + b'\n')


def new_artifact(build_state, artifact_name, sources=None, source_obj=None,
                 extra=None, config_hash=None,
                 render_template_into=render_template_into):
    """Create a new artifact and returns it."""
    dst_filename = build_state.get_destination_filename(artifact_name)
    key = build_state.artifact_name_from_destination_filename(dst_filename)
    artifact = Artifact(
        build_state, key, dst_filename, sources, source_obj=source_obj,
        extra=extra, config_hash=config_hash)
    artifact.render_template_into = types.MethodType(render_template_into,
                                                     artifact)
    return artifact


class AmpPlugin(Plugin):
    """Use lektor plugin mechanism to extend an artifact for amp."""

    name = u'AMP'
    description = u'Create an amp version of your website.'

    def on_before_build_all(self, builder, **extra):
        """Set and report if the amp shall be genereated."""
        self.amp = strtobool(self.get_config().get('generate_amp') or 'True')
        msg = 'Generate AMP' if self.amp else 'Generate AMP turned off'
        reporter.report_generic(msg)

    def on_before_build(self, source, prog, **extra):
        """Extend Artifact to generate an amp sub_artifact."""
        if self.amp:
            prog.build_state.new_artifact = types.MethodType(new_artifact,
                                                             prog.build_state)
