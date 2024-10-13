# defmodule Ping do
#   def start do
#     # receive pattern matches on a series of potential messages and runs some
#     # code when it receives that message. Here we'll just send a message to the
#     # pid we're sent.
#     receive do
#       {:pong, from} -> send(from, {:ping, self()})
#     end
#   end
# end

defmodule Ping do
  def start do
    loop()
  end

# It's worth talking a little bit about how receive works. Processes have a mailbox, and any messages sent to a process queue up in a list in the mailbox. receive will look at the mailbox, and handle the first message it finds in the order specified in the call to receive. If there are no messages, it blocks until there is a message.
  def loop do
    receive do
      {:pong, from} ->
        IO.puts "ping ->"
        :timer.sleep 500
        send(from, {:ping, self()})
      {:ping, from} ->
        IO.puts "            <- pong"
        :timer.sleep 500
        send(from, {:pong, self()})
    end
    loop()
  end
end
