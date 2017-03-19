# -*- coding: utf-8 -*-

# Copyright (c) 2016, Chintalagiri Shashank
#
# This Sphinx Extension is made available under the BSD 2-clause License. See
# sphinxcontrib's LICENSE file for the full text.

import os
import shutil
import subprocess

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.images import Image


class SQLAlchemyViz(Image):

    option_spec = {'metadataobject': directives.unchanged}
    required_arguments = 0

    def run(self):
        if self.content:
            error = self.state_machine.reporter.error(
                """The SQLAlchemyViz directive does not know what to
                do with provided content""",
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno
            )
            return [error]

        env = self.state.document.settings.env  # sphinx.environment.BuildEnvironment
        config = env.config                     # sphinx.config.Config
        output_folder = os.path.abspath(
                os.path.join(env.srcdir, config["html_static_path"][0])
        )

        # Get the path to the object containing the metadata
        metadatapath = self.options.get('metadataobject', None)
        if metadatapath is None:
            error = self.state_machine.reporter.error(
                "SQLAlchemyViz needs to be given the object"
                "containing the SQLAlchemy metadata as the :metadataobject: "
                "parameter",
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno
            )
            return [error]
        output_path = os.path.join(output_folder, metadatapath + '.png')
        metadata = ':'.join(metadatapath.rsplit('.', 1))
        sqlaviz_cmd = ['sqlaviz',
                       '-p neato',            # workaround newtrap bug.
                       '--unique-relations',
                       #'--show-constraints', # workaround neato bug(?)
                       metadata,
                       # workaround broken syntax bug post update
                       '-o node_margin=\'"0,0"\'',
                       '-f out.dot']

        devnull = open(os.devnull)
        print ' '.join(sqlaviz_cmd)
        sqlaviz_sp = subprocess.Popen(' '.join(sqlaviz_cmd),
                                      stdout=devnull,
                                      stderr=devnull,
                                      shell=True)
        sqlaviz_sp.communicate()

        render_cmd = 'ccomps -x out.dot | dot | gvpack -array3 ' \
                     '| neato -Tpng -n2 -o out.png'
        render_sp = subprocess.Popen(render_cmd,
                                     stdout=devnull,
                                     stderr=devnull,
                                     shell=True)
        render_sp.communicate()
        devnull.close()

        try:
            shutil.move('out.png', output_path)
            os.remove('out.dot')

            relpath = os.path.relpath(output_path, env.srcdir)
            # I'm exhausted.
            self.arguments.insert(0, '/' + relpath)
        except IOError:
            error = self.state_machine.reporter.error(
                "sqlaviz was unable to generate the output image!",
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno
            )
            return [error]
        return Image.run(self)


def setup(app):
    app.add_directive('sqlaviz', SQLAlchemyViz)
    return {'version': '0.1'}
