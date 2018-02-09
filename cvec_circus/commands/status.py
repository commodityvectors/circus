from cvec_circus.commands.base import Command
from cvec_circus.exc import ArgumentError


class Status(Command):
    """\
        Get the status of a watcher or all watchers
        ===========================================

        This command start get the status of a watcher or all watchers.

        ZMQ Message
        -----------

        ::

            {
                "command": "status",
                "properties": {
                    "name": '<name>",
                }
            }

        The response return the status "active" or "stopped" or the
        status / watchers.


        Command line
        ------------

        ::

            $ cvec_circusctl status [<name>]

        Options
        +++++++

        - <name>: name of the watcher

        Example
        +++++++

        ::

            $ cvec_circusctl status dummy
            active
            $ cvec_circusctl status
            dummy: active
            dummy2: active
            refuge: active

    """

    name = "status"

    def message(self, *args, **opts):
        if len(args) > 1:
            raise ArgumentError("message invalid")

        if len(args) == 1:
            return self.make_message(name=args[0])
        else:
            return self.make_message()

    def execute(self, arbiter, props):
        if 'name' in props:
            watcher = self._get_watcher(arbiter, props['name'])
            return {"status": watcher.status()}
        else:
            return {"statuses": arbiter.statuses()}

    def console_msg(self, msg):
        if "statuses" in msg:
            statuses = msg.get("statuses")
            watchers = sorted(statuses)
            return "\n".join(["%s: %s" % (watcher, statuses[watcher])
                              for watcher in watchers])
        elif "status" in msg and "status" != "error":
            return msg.get("status")
        return self.console_error(msg)
